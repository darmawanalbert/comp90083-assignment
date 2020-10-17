from mesa import Agent
from road_network_model.constant import DIRECTION, CAR_STATE, GRID_HEIGHT, GRID_WIDTH
import math

class Car(Agent):
    X_COOR = 0
    Y_COOR = 1

    def __init__(self,
                unique_id,
                plate_number_oddity,
                source_coor,
                destination_coor,
                car_direction,
                max_speed,
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
        self.max_speed = max_speed
        self.next_coor = (0,0)
        self.next_state = None

        print(self.destination_coor)

    def neighbors(self):
        neighbors = self.model.grid.neighbor_iter(
                        (self.current_coor[Car.X_COOR],
                        self.current_coor[Car.Y_COOR]), # False = only takes Von Neumann neighbours
                        True) # True = includes centre

        return neighbors
    
    def getCrowDistance(self, coor1, coor2):
        distance = math.sqrt(
            ((coor1[self.X_COOR]-coor2[self.X_COOR]) **2) + ((coor1[self.Y_COOR]-coor2[self.Y_COOR]) **2)
            )

        return distance

    # SimultaneousActivation required two methods: step and advance
    def step(self):
        """ step """
        # Get neighbours
        neighbors = self.neighbors()
        layout = self.model.map.get_layout()
        new_direction = layout[self.current_coor[0]][self.current_coor[1]]
        
        test = self.model.map.get_exit_point((46, 2),">",layout[46][2])
        print("test: ", test)

        #print("new direction: ", new_direction)
        #print("exit dir: ", self.exit_direction)
        if new_direction not in DIRECTION:
            new_direction = self.exit_direction
            next_coor_x = self.current_coor[0] + DIRECTION[new_direction][0]
            next_coor_y = self.current_coor[1] + DIRECTION[new_direction][1]
            self.current_direction = new_direction
        else:
            #print("new_direction ", self.current_coor, " : ", new_direction)
            self.current_direction = new_direction
            #new_direction = self.current_direction
        
        # get successing location after action
        if layout[self.current_coor[0]][self.current_coor[1]] == 'T':
            # should find the shortest path to destination, but for now simplify using distance measurements
            shortestDist = float("inf")
            new_x = self.current_coor[0]
            new_y = self.current_coor[1]
            #print("HI")
            for direction in DIRECTION:
                #print(direction)
                temp_x = self.current_coor[0] + DIRECTION[direction][0]
                temp_y = self.current_coor[1] + DIRECTION[direction][1]
                
                newDist = self.getCrowDistance((temp_x, temp_y), self.destination_coor)
                if newDist < shortestDist:
                    shortestDist = newDist
                    best_action = direction

                    new_x = temp_x
                    new_y = temp_y
            
            new_direction = best_action
            self.current_direction = new_direction

        else:
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
                #if current_direction == 'NORTH' or current_direction == 'SOUTH':
                    # Adjacent cars are in west and east
                #else:
                    # Adjacent cars are in north and south
        if car_in_front:
            if front_neighbor.current_state == "IDLE":
                new_state = "IDLE"
                self.current_state = new_state
            else:
                self.next_coor = (new_x, new_y)
        else:
            self.next_coor = (new_x, new_y)

        #Get direction
        #print(self.current_state)
            #self.next_coor[Car.X_COOR] = self.current_coor[Car.X_COOR] + DIRECTION[self.current_direction][0]
            #self.next_coor[Car.Y_COOR] = self.current_coor[Car.Y_COOR] + DIRECTION[self.current_direction][1]

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
