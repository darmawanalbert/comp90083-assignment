from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector

from road_network_model.agent import Car, Road, Office, Residence, Entertainment, TrafficLight
from road_network_model.map import MapGenerator
from road_network_model.constant import DIRECTION, CAR_STATE, DAY, COLOR

from road_network_model.util import get_euclidean_distance

import math
import random

class RoadNetworkModel(Model):
    description = (
        "A model for simulating Road Network Model"
    )

    def __init__(self, number_of_cars, width, height, is_odd_even_policy_enabled, policy_1_start_time, policy_1_duration, policy_2_start_time, policy_2_duration):
        # Tick increment
        self.tick = 0

        # Mean Travel Time
        self.mean_travel_time = 1.23

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

        self.policy_1_start_time = policy_1_start_time
        self.policy_1_duration = policy_1_duration
        self.policy_2_start_time = policy_2_start_time
        self.policy_2_duration = policy_2_duration

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
        proportion_of_office_workers = DAY[self.day]
        number_of_office_workers = math.ceil(proportion_of_office_workers * number_of_cars)
        number_of_shopper = number_of_cars - number_of_office_workers

        office_list = []
        while len(office_list) <= number_of_office_workers:
            office_list.append(office[self.random.randint(0, len(office) -1)])

        entertainment_list = []
        while len(entertainment_list) <= number_of_shopper:
            entertainment_list.append(entertainment[self.random.randint(0, len(entertainment) - 1)])

        office_entertainment_list = office_list + entertainment_list
        random.shuffle(residence_list)
        print("Residence List: ", residence_list)

        layout = self.map.get_layout()
        for i in range(number_of_cars):
            plate_number_oddity = self.random.randint(0, 1)
            source_x = residence_list[i][0]
            source_y = residence_list[i][1]
            destination_x = office_entertainment_list[i][0]
            destination_y = office_entertainment_list[i][1]

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

            car_state = "IDLE"
            departure_time = self.random.randint(0,5)
            return_time = float("inf")

            car = Car(i, plate_number_oddity,
                        (source_x,source_y),
                        (destination_x,destination_y),
                        car_direction,
                        car_state,
                        departure_time,
                        return_time,
                        self)

            self.grid.place_agent(car, (source_x,source_y))
            self.schedule.add(car)

    def step(self):
        self.schedule.step()
        self.tick += 1

        # After 4 days (5760 minutes), stop the simulation
        if self.tick >= 5760:
            self.running = False

        # Check whether a day (1440 minutes) has passed
        if self.tick % 1440 == 0:
            self.day += 1
            self.is_odd_date = not self.is_odd_date

    def is_plate_number_oddity_allowed(self, plate_number_oddity=0, xy=(0, 0)):
        x, y = xy

        # implement odd even policy for avenue only.
        if(self.map.is_avenue(x, y)):
            if(self.is_odd_date == True):
                if(plate_number_oddity % 2 == 0):
                    return True
                else:
                    return False
            else:
                if(plate_number_oddity % 2 == 1):
                    return True
                else:
                    return False
        else:
            return True

    def is_odd_even_policy_time(self):
        #1 day == 1440 minutes
        day_tick = self.tick % 1440

        print("day_tick:", day_tick)
        print("self.policy_1_start_time : ", self.policy_1_start_time)
        print("self.policy_1_duration: ", self.policy_1_duration)
        print("self.policy_2_start_time : ", self.policy_2_start_time)
        print('self.policy_2_duration:', self.policy_2_duration)
        #period 1
        if day_tick >= self.policy_1_start_time * 60 and day_tick <= (self.policy_1_start_time + self.policy_1_duration) * 60:
            return True
        #period 2
        elif day_tick >= self.policy_2_start_time * 60 and day_tick <= (self.policy_2_start_time + self.policy_2_duration) * 60:
            return True
        else:
            return False
