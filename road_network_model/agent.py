from mesa import Agent
from road_network_model.constant import DIRECTION, CAR_STATE, GRID_HEIGHT, GRID_WIDTH, INTERSECTION, BUILDING, INTERSECTION_SIGN
import math
from road_network_model.util import get_euclidean_distance, get_next_direction

class Car(Agent):
    X_COOR = 0
    Y_COOR = 1

    def __init__(self,
                unique_id,
                plate_number_oddity,
                source_coor,
                destination_coor,
                car_direction,
                car_state,
                model):
        super().__init__(unique_id,model)
        self.plate_number_oddity = plate_number_oddity # ODD or EVEN, 0 is even and 1 is odd
        self.current_coor = source_coor
        self.source_coor = source_coor
        self.destination_coor = destination_coor
        self.exit_direction = car_direction
        self.current_direction = car_direction
        self.current_state = car_state
        self.next_coor = (0,0)
        self.next_state = None
        self.shortest_exit_point = None

        print(self.destination_coor)

    def neighbors(self):
        neighbors = self.model.grid.neighbor_iter(
                        (self.current_coor[Car.X_COOR],
                        self.current_coor[Car.Y_COOR]), # False = only takes Von Neumann neighbours
                        True) # True = includes centre

        return neighbors

    # SimultaneousActivation required two methods: step and advance
    def step(self):
        """ step """
        # Map Information
        map_instance = self.model.map
        layout = map_instance.get_layout()

        # Get neighbours
        neighbors = self.neighbors()
        new_direction = layout[self.current_coor[0]][self.current_coor[1]]

        # Determine Car direction
        # Inside a Office / Residence / Entertaint
        if new_direction in BUILDING:
            new_direction = self.exit_direction
            next_coor_x = self.current_coor[0] + DIRECTION[new_direction][0]
            next_coor_y = self.current_coor[1] + DIRECTION[new_direction][1]
            self.current_direction = new_direction
        # Encounter an intersection
        elif new_direction in INTERSECTION_SIGN:
            current_pos = (self.current_coor[0], self.current_coor[1])
            intersection_type = layout[self.current_coor[0]][self.current_coor[1]]
            exit_points = map_instance.get_exit_point(current_pos, self.current_direction, intersection_type)

            shortest_distance = float("inf")
            shortest_exit_point = ()
            for exit_point in exit_points:
                newDist =  get_euclidean_distance(exit_point[0], self.current_coor)
                if newDist < shortest_distance:
                    shortest_distance = newDist
                    shortest_exit_point = exit_point[0]

            print("exit_points: ", exit_points, ", shortest_exit_point: ", shortest_exit_point)
            self.shortest_exit_point = shortest_exit_point

            print("self.current_direction:", self.current_direction, ", self.current_coor:", self.current_coor)
            print("layout[self.shortest_exit_point[0]][self.shortest_exit_point[1]]:",layout[self.shortest_exit_point[0]][self.shortest_exit_point[1]])
            print("self.shortest_exit_point: ", self.shortest_exit_point)

            local_current_direction = get_next_direction(self.current_direction, self.current_coor, layout[self.shortest_exit_point[0]][self.shortest_exit_point[1]], self.shortest_exit_point)

            new_x = self.current_coor[0] + DIRECTION[local_current_direction][0]
            new_y = self.current_coor[1] + DIRECTION[local_current_direction][1]
            if new_x < 0 or new_x == GRID_WIDTH:
                new_x = self.current_coor[0]
            if new_y < 0 or new_y == GRID_HEIGHT:
                new_y = self.current_coor[1]

            self.next_coor = (new_x, new_y)
            print("local_current_direction: ", local_current_direction)

        # Inside a Road
        elif new_direction == "x":
            local_current_direction = get_next_direction(self.current_direction, self.current_coor, layout[self.shortest_exit_point[0]][self.shortest_exit_point[1]], self.shortest_exit_point)

            new_x = self.current_coor[0] + DIRECTION[local_current_direction][0]
            new_y = self.current_coor[1] + DIRECTION[local_current_direction][1]
            if new_x < 0 or new_x == GRID_WIDTH:
                new_x = self.current_coor[0]
            if new_y < 0 or new_y == GRID_HEIGHT:
                new_y = self.current_coor[1]

            self.next_coor = (new_x, new_y)
            print("local_current_direction: ", local_current_direction)

        else:
            self.current_direction = new_direction
            new_x = self.current_coor[0] + DIRECTION[self.current_direction][0]
            new_y = self.current_coor[1] + DIRECTION[self.current_direction][1]
            if new_x < 0 or new_x == GRID_WIDTH:
                new_x = self.current_coor[0]
            if new_y < 0 or new_y == GRID_HEIGHT:
                new_y = self.current_coor[1]

        car_in_front = False
        front_neighbor = None
        for neighbor in neighbors:
            if isinstance(neighbor, Car):
                # Check whether the neighbour car is in front
                if neighbor.current_coor == (new_x, new_y):
                    car_in_front = True
                    front_neighbor = neighbor
        if car_in_front:
            if front_neighbor.current_state == "IDLE":
                new_state = "IDLE"
                self.current_state = new_state
            else:
                self.next_coor = (new_x, new_y)
        else:
            self.next_coor = (new_x, new_y)

    def advance(self):
        """ advance """
        self.current_coor = self.next_coor
        #self.current_state = self.next_state
        self.model.grid.move_agent(self, self.next_coor)

class Road(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model

    def getDirections(self):
        self.model.map.get_road_position()

    def getRoadPosition(self):
        return self.model.map.get_road_position()

class Office(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model

class Entertaint(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model

class Residence(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model

class TrafficLight(Agent):
    def __init__(self, unique_id, pos, model, color):
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model
        self.color = color

    def step(self):
        print("hello!") ## wait...

    def advance(self):
        self.current_coor = self.next_coor
        self.model.grid.move_agent(self, self.next_coor)
