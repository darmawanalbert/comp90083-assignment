from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector

from road_network_model.agent import Car, Road, Office, Residence, Entertaint
from road_network_model.map import MapGenerator
from road_network_model.constant import DIRECTION, CAR_STATE, DAY

from road_network_model.util import getCrowDistance

import math

class RoadNetworkModel(Model):
    description = (
        "A model for simulating Road Network Model"
    )

    def __init__(self, number_of_cars, width, height):
        # Tick increment
        self.tick = 0

        # Set the day of the week
        self.day = "THU"

        # Set up Spatial dimension
        self.grid = MultiGrid(width, height, True)

        # Set up Temporal dimension
        self.schedule = SimultaneousActivation(self)
        self.running = True

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
        
        ## generate entertaint
        entertaintPosition = self.map.get_entertaint_position()
        for i in range(len(entertaintPosition)):
            entertaint = Entertaint(i, entertaintPosition[i], self)
            self.grid.place_agent(entertaint, entertaintPosition[i])

        # Get source and destination lists
        source_list = self.map.get_residence_position()
        office = self.map.get_office_position()
        entertainment = self.map.get_entertaint_position()
        print(entertainment)

        # Create destination list based on weekday/weekend proportion
        proportion_of_office_workers = DAY[self.day]
        number_of_office_workers = math.ceil(proportion_of_office_workers * number_of_cars)
        number_of_shopper = 1 - number_of_office_workers

        office_list = []
        entertainment_list = []
        worker = 0
        shopper = 0
        while worker <= number_of_office_workers:
            office_list.append(office[self.random.randint(0, len(office) -1)])
            worker += 1
        while shopper <= number_of_shopper:
            entertainment_list.append(entertainment[self.random.randint(0, len(entertainment) - 1)])
            shopper += 1
        
        print(office_list)
        print(entertainment_list)
        
        """# Create a set of initial car positions
        initial_car_position = set() # set? so no two cars can start from the same position?
        while len(initial_car_position) != number_of_cars:
            random_road_index = self.random.randint(0, len(roadPosition) - 1)
            initial_car_position.add(random_road_index)"""
        
        initial_car_position = []  # list or set? if set, we might have more cars than sources
        while len(initial_car_position) != number_of_cars:
            random_road_index = self.random.randint(0, len(source_list) - 1)
            initial_car_position.append(source_list[random_road_index])
        #print(initial_car_position)
        
        layout = self.map.get_layout()
        for i in range (number_of_cars):
            plate_number_oddity = self.random.randint(0, 1)
            """current_index = initial_car_position.pop()
            source_x = roadPosition[current_index][0]
            source_y = roadPosition[current_index][1]"""
            # Randomising car sources
            random_position = initial_car_position.pop()
            source_x = random_position[0]
            #print(source_x)
            source_y = random_position[1]
            #print(source_y)

            # Randomising car destinations
            randomise_destination = self.random.randint(0, 1)
            if randomise_destination == 0: # office worker, given proportion hasn't been met
                if len(office_list) > 0:
                    random_position = office_list.pop()
                    destination_x = random_position[0]
                    destination_y = random_position[0]
                else:
                    random_position = entertainment_list.pop()
                    destination_x = random_position[0]
                    destination_y = random_position[0]
            else:
                if len(entertainment_list) > 0:
                    random_position = entertainment_list.pop()
                    destination_x = random_position[0]
                    destination_y = random_position[0]
                else:
                    random_position = office_list.pop()
                    destination_x = random_position[0]
                    destination_y = random_position[0]
            
            max_speed = 100
            stateFringes = self.map.get_successors(source_x, source_y)
            shortestDist = float("inf")
            for stateFringe in stateFringes:
                current_direction =  stateFringe[1] # "^" "v" ">" "<"
                print(stateFringe[0])
                if current_direction in DIRECTION:
                    temp_x = stateFringe[0][0] + DIRECTION[current_direction][0]
                    temp_y = stateFringe[0][1] + DIRECTION[current_direction][1]

                    newDist = getCrowDistance((temp_x, temp_y), (destination_x, destination_y))
                    if newDist < shortestDist:
                        shortestDist = newDist
                        car_direction = current_direction
                        print((source_x, source_y), car_direction)

            #print(car_direction)
            car_state = "IDLE"

            car = Car(i, plate_number_oddity,
                        (source_x,source_y),
                        (destination_x,destination_y),
                        car_direction,
                        max_speed,
                        car_state, self)
            print("car direction: ", car_direction)

            self.grid.place_agent(car, (source_x,source_y))
            self.schedule.add(car)

    def step(self):
        self.schedule.step()
        self.tick += 1
        print(self.tick)
