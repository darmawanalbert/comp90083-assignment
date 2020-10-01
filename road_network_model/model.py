from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector

from road_network_model.agent import Car, Road, Building
from road_network_model.map import MapGenerator
from road_network_model.constant import DIRECTION, CAR_STATE

class RoadNetworkModel(Model):
    description = (
        "A model for simulating Road Network Model"
    )

    def __init__(self, number_of_cars, width, height):
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

        ## generate building
        buildingPosition = self.map.get_building_position()
        for i in range(len(buildingPosition)):
            building = Building(i, buildingPosition[i], self)
            self.grid.place_agent(building, buildingPosition[i])

        # Create a set of initial car positions
        initial_car_position = set()
        while len(initial_car_position) != number_of_cars:
            random_road_index = self.random.randint(0, len(roadPosition) - 1)
            initial_car_position.add(random_road_index)

        layout = self.map.get_layout()
        for i in range (number_of_cars):
            plate_number_oddity = self.random.randint(0, 1)
            current_index = initial_car_position.pop()
            source_x = roadPosition[current_index][0]
            source_y = roadPosition[current_index][1]
            destination_x = 0
            destination_y = 0
            max_speed = 100
            car_direction = layout[source_x][source_y] # "^" "v" ">" "<"
            #print(car_direction)
            car_state = "IDLE"

            car = Car(i, plate_number_oddity,
                        (source_x,source_y),
                        (destination_x,destination_y),
                        car_direction,
                        max_speed,
                        car_state, self)

            self.grid.place_agent(car, (source_x,source_y))
            self.schedule.add(car)


    def step(self):
        self.schedule.step()
