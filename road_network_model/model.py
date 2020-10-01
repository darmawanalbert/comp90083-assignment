from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector

from road_network_model.agent import Car, Road
from road_network_model.map import MapGenerator
from road_network_mode.constant import DIRECTION

class RoadNetworkModel(Model):
    description = (
        "A model for simulating Road Network Model"
    )

    def __init__(self, number_of_cars, width, height):
        # Set up Spatial dimension
        self.grid = MultiGrid(width, height, True)

        # Set up Temporal dimension
        self.schedule = SimultaneousActivation(self)

        for i in range (number_of_cars):
            plate_number_oddity = self.random.randint(0, 1)

            source_x = self.random.randrange(self.grid.width)
            source_y = self.random.randrange(self.grid.height)
            destination_x = 0
            destination_y = 0
            max_speed = 100
            car_direction = self.random.choice(DIRECTION.keys()) # to be changed

            car = Car(i, plate_number_oddity, [source_x,source_y], (destination_x,destination_y), max_speed, car_direction, self)
            self.grid.place_agent(car, (source_x,source_y))

        ## generate road
        mapGenerator = MapGenerator()
        roadPosition = mapGenerator.generate_road_position()
        for i in range(len(roadPosition)):
            road = Road(i, roadPosition[i], self)
            self.grid.place_agent(road, roadPosition[i])

        ## generate building

    def step(self):
        self.schedule.step()
