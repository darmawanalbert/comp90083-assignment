from mesa import Agent
from road_network_model.constant import DIRECTION, CAR_STATE

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
        self.plate_number_oddity = plate_number_oddity # ODD or EVEN
        self.current_coor = source_coor
        self.destination_coor = destination_coor
        self.current_direction = car_direction
        self.current_state = car_state
        self.max_speed = max_speed
        self.next_coor = None

    def neighbors(self):
        neighbors = self.model.grid.neighbor_iter(
                        (self.current_coor[X_COOR],
                        self.current_coor[Y_COOR]), 
                        False, # False = only takes Von Neumann neighbours
                        True) # True = includes centre

        return neighbors

    # SimultaneousActivation required two methods: step and advance
    def step(self):
        """ step """
        # Get neighbours
        neighbors = self.neighbors()

        for neighbor in neighbors:
        # if neighbor[X_COOR] == self.current_coor[X_COOR]:
            #print(neighbor)
            if neighbor.isType(Car):
                # Check whether there is a car in front
                if neighbor.current_coor == self.current_coor + DIRECTION[self.current_direction]:
                    front_neighbor = neighbor
                    if front_neighbor.current_state == "IDLE":
                        self.current_state == "IDLE"

                #if current_direction == 'NORTH' or current_direction == 'SOUTH':
                    # Adjacent cars are in west and east
                #else:
                    # Adjacent cars are in north and south
        
         #Get direction
            if self.current_state != "IDLE":
                self.next_state == self.current_state
            #else:


    def advance(self):
        """ advance """
        self.current_coor = self.next_coor


class Road(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model
    
    def getDirections(self):
        self.model.map.get_road_position() 

    def getRoadPosition(self):
        return self.model.map.get_road_position()

class Building(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model