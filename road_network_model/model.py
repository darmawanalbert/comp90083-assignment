from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector

from road_network_model.agent import Car, Road, Office, Residence, Entertainment, TrafficLight
from road_network_model.map import MapGenerator
from road_network_model.constant import DIRECTION, CAR_STATE, DAY, COLOR, PEAK_HOURS, ACTIVITY_PROPORTION

from road_network_model.util import get_euclidean_distance

import math
import random
import numpy as np


# Data Collection method
def number_idle_cars(model):
    return sum([1 for j in range(100) for i in range(100) for cell in model.grid.iter_cell_list_contents((i,j))
            if type(cell) is Car and cell.current_state == "IDLE"])

def number_move_cars(model):
    return sum([1 for j in range(100) for i in range(100) for cell in model.grid.iter_cell_list_contents((i,j))
            if type(cell) is Car and cell.current_state == "MOVE"])

def number_finished_cars(model):
    return sum([1 for j in range(100) for i in range(100) for cell in model.grid.iter_cell_list_contents((i,j))
            if type(cell) is Car and cell.current_state == "FINISHED"])

# TODO: Remove later
def number_office(model):
    return sum([1 for j in range(100) for i in range(100) for cell in model.grid.iter_cell_list_contents((i,j))
            if type(cell) is Car and cell.arrive_at_destination == 0])

def number_residence(model):
    return sum([1 for j in range(100) for i in range(100) for cell in model.grid.iter_cell_list_contents((i,j))
            if type(cell) is Car and cell.arrive_at_destination == 1])

def simulation_minutes(model):
    return model.tick

def mean_travel_time(model):
    return model.mean_travel_time

class RoadNetworkModel(Model):
    description = (
        "A model for simulating Road Network Model"
    )

    def __init__(self, number_of_cars, width, height, is_odd_even_policy_enabled, policy_range_time):
        # Tick increment
        self.tick = 0

        # Mean Travel Time
        self.mean_travel_time = 0.0

        # Odd-Even Policy Enabled
        self.is_odd_even_policy_enabled = is_odd_even_policy_enabled

        # Set the day of the week
        self.day = 1
        self.is_odd_date = True

        # Set up Spatial dimension
        self.grid = MultiGrid(width, height, True)

        # Set up Temporal dimension
        self.schedule = SimultaneousActivation(self)
        self.running = True

        self.policy_range_time = policy_range_time

        print("Policy Range Time: ", self.policy_range_time)

        # Set up peak hours
        self.start_peak_hour_1 = PEAK_HOURS["START_PEAK_HOUR_1"] #7
        self.end_peak_hour_1 = PEAK_HOURS["END_PEAK_HOUR_1"] #10
        self.start_peak_hour_2 = PEAK_HOURS["START_PEAK_HOUR_2"] #4
        self.end_peak_hour_2 = PEAK_HOURS["END_PEAK_HOUR_2"] #7

        # Set number_of_cars
        self.num_of_cars = number_of_cars

        # Car distribution
        num_highly_active_cars = math.ceil(ACTIVITY_PROPORTION["HIGHLY_ACTIVE"] * number_of_cars)
        num_business_hours_cars = math.ceil(ACTIVITY_PROPORTION["BUSINESS_HOURS"] * number_of_cars)
        num_peak_hours_cars = number_of_cars - (num_highly_active_cars + num_business_hours_cars)

        ## generate road
        self.map = MapGenerator()
        roadPosition = self.map.get_road_position()
        for i in range(len(roadPosition)):
            road = Road(i, roadPosition[i], self)
            self.grid.place_agent(road, roadPosition[i])

        ## generate office
        officePosition = self.map.get_office_position()
        for i in range(len(officePosition)):
            office = Office(i, officePosition[i], self)
            self.grid.place_agent(office, officePosition[i])

        ## generate residence
        residencePosition = self.map.get_residence_position()
        for i in range(len(residencePosition)):
            residence = Residence(i, residencePosition[i], self)
            self.grid.place_agent(residence, residencePosition[i])

        ## generate entertainment
        entertainmentPosition = self.map.get_entertainment_position()
        for i in range(len(entertainmentPosition)):
            entertainment = Entertainment(i, entertainmentPosition[i], self)
            self.grid.place_agent(entertainment, entertainmentPosition[i])

        ## generate traffic light
        trafficLightPosition = self.map.get_traffic_light_position()
        for i in range(len(trafficLightPosition)):
            trafficLight = TrafficLight(i, trafficLightPosition[i], self, COLOR["dark_grey"])
            self.grid.place_agent(trafficLight, trafficLightPosition[i])

        # Get source and destination lists
        residence_list = self.map.get_residence_position()
        office = self.map.get_office_position()
        entertainment = self.map.get_entertainment_position()


        # Create destination list based on weekday/weekend proportion
        """proportion_of_office_workers = DAY[self.day]
        number_of_office_workers = math.ceil(proportion_of_office_workers * number_of_cars)
        number_of_shopper = number_of_cars - number_of_office_workers

        office_list = []
        while len(office_list) <= number_of_office_workers:
            office_list.append(office[self.random.randint(0, len(office) -1)])

        entertainment_list = []
        while len(entertainment_list) <= number_of_shopper:
            entertainment_list.append(entertainment[self.random.randint(0, len(entertainment) - 1)])
        
        office_entertainment_list = office_list + entertainment_list"""

        number_of_office_workers, number_of_shopper = self.get_number_of_workers_and_shoppers(DAY[self.day], number_of_cars)
        self.office_entertainment_list = self.get_random_office_entertainment_list(office, number_of_office_workers, entertainment, number_of_shopper)
        random.shuffle(residence_list)
        # print("Residence List: ", residence_list)

        layout = self.map.get_layout()
        for i in range(number_of_cars):
            # determine departure and return time based on activity level
            if i <= num_highly_active_cars:
                activity_level = "HIGHLY_ACTIVE"
                departure_time = 0
                return_time = float("inf")
            elif i <= num_business_hours_cars:
                activity_level = "BUSINESS_HOURS"
                departure_time = self.start_peak_hour_1
                return_time = float("inf")
            else:
                activity_level = "PEAK_HOURS"
                departure_time = self.random.randint(self.start_peak_hour_1,self.end_peak_hour_1)
                return_time = self.random.randint(self.start_peak_hour_2,self.end_peak_hour_2)

            plate_number_oddity = self.random.randint(0, 1)
            #plate_number_oddity = 0
            source_x = residence_list[i][0]
            source_y = residence_list[i][1]
            destination_x = self.office_entertainment_list[i][0]
            destination_y = self.office_entertainment_list[i][1]

            # TODO: Remove this later
            # source_x = 58
            # source_y = 92
            # destination_x = 58
            # destination_y = 85

            state_fringes = self.map.get_fringes(source_x, source_y)
            shortest_distance = float("inf")
            car_direction = state_fringes[0][1]
            for state_fringe in state_fringes:
                current_direction =  state_fringe[1] # "^" "v" ">" "<"
                if current_direction in DIRECTION:
                    temp_x = state_fringe[0][0] + DIRECTION[current_direction][0]
                    temp_y = state_fringe[0][1] + DIRECTION[current_direction][1]

                    newDist = get_euclidean_distance((temp_x, temp_y), (destination_x, destination_y))
                    if newDist < shortest_distance:
                        shortest_distance = newDist
                        car_direction = current_direction
            
            # all cars are initialised as IDLE
            car_state = "IDLE"

            car = Car(i, plate_number_oddity,
                        (source_x,source_y),
                        (destination_x,destination_y),
                        car_direction,
                        car_state,
                        departure_time,
                        return_time,
                        activity_level,
                        self)

            self.grid.place_agent(car, (source_x,source_y))
            self.schedule.add(car)

        # Data Collection
        self.datacollector = DataCollector({
            "Idle": number_idle_cars,
            "Move": number_move_cars,
            "Finished": number_finished_cars,
            "SimulationMinutes": simulation_minutes,
            "NumberOffice": number_office,
            "NumberResidence": number_residence,
            "MeanTravelTime": mean_travel_time
        })
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.tick += 1
        self.mean_travel_time = np.mean([cell.travel_time for j in range(100) for i in range(100) for cell in self.grid.iter_cell_list_contents((i,j))
            if type(cell) is Car])
        self.datacollector.collect(self)
        print(self.tick)
        # After 4 days (5760 minutes), stop the simulation
        if self.tick >= 5760:
            self.running = False

        # Check whether a day (1440 minutes) has passed
        if self.tick % 1440 == 0:
            self.day += 1
            self.is_odd_date = not self.is_odd_date

            # Create new destination lists
            office = self.map.get_office_position()
            entertainment = self.map.get_entertainment_position()
            number_of_office_workers, number_of_shopper = self.get_number_of_workers_and_shoppers(
                DAY[self.day], self.num_of_cars)
            self.office_entertainment_list = self.get_random_office_entertainment_list(
                office, number_of_office_workers, 
                entertainment, number_of_shopper)
            
            print(self.office_entertainment_list)

    def is_plate_number_oddity_allowed(self, plate_number_oddity=0, xy=(0, 0)):
        x, y = xy
        # print("plate_number_oddity: ", plate_number_oddity)
        # print("xy: ", xy)
        # implement odd even policy for avenue only.
        if(self.map.is_avenue(x, y)):
            if(self.is_odd_date == True): # date is odd
                if(plate_number_oddity % 2 == 1): # plate is odd
                    return True
                else:
                    return False
            else: # date is even
                if(plate_number_oddity % 2 == 0): # plate is even
                    return True
                else:
                    return False
        else:
            return True

    def is_odd_even_policy_time(self):
        #1 day == 1440 minutes
        day_tick = self.tick % 1440

        # print("day_tick:", day_tick)
        # print("self.policy_range_time : ", self.policy_range_time)
        
        if self.policy_range_time == '7_10_and_16_19':
            if day_tick >= (7 * 60) and day_tick <= (10 * 60):
                return True
            elif day_tick >= (16 * 60) and day_tick <= (19 * 60):
                return True
            else:
                return False
        elif self.policy_range_time == '8_11_and_17_20':
            if day_tick >= (8 * 60) and day_tick <= (11 * 60):
                return True
            elif day_tick >= (17 * 60) and day_tick <= (20 * 60):
                return True
            else:
                return False
        elif self.policy_range_time == '6_9_and_15_18':
            if day_tick >= (6 * 60) and day_tick <= (9 * 60):
                return True
            elif day_tick >= (15 * 60) and day_tick <= (18 * 60):
                return True
            else:
                return False
        elif self.policy_range_time == '8_9_and_17_18':
            if day_tick >= (8 * 60) and day_tick <= (9 * 60):
                return True
            elif day_tick >= 17 * 60 and day_tick <= 18 * 60:
                return True
            else:
                return False
        elif self.policy_range_time == '6_11_and_15_20':
            if day_tick >= (6 * 60) and day_tick <= (11 * 60):
                return True
            elif day_tick >= (15 * 60) and day_tick <= (20 * 60):
                return True
            else:
                return False
        else:
            return False
    
    def get_number_of_workers_and_shoppers(self, proportion_of_office_workers, number_of_cars):
        number_of_office_workers = math.ceil(proportion_of_office_workers * number_of_cars)
        number_of_shopper = number_of_cars - number_of_office_workers

        return number_of_office_workers, number_of_shopper
    
    def get_random_office_entertainment_list(self, office, number_of_office_workers, entertainment, number_of_shopper):
        office_list = []
        while len(office_list) <= number_of_office_workers:
            office_list.append(office[self.random.randint(0, len(office) - 1)])

        entertainment_list = []
        while len(entertainment_list) <= number_of_shopper:
            entertainment_list.append(
                entertainment[self.random.randint(0, len(entertainment) - 1)])

        office_entertainment_list = office_list + entertainment_list

        return office_entertainment_list
