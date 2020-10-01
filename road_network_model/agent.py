from mesa import Agent
from road_network_model.constant import DIRECTION

class Car(Agent):
    X_COOR = 0
    Y_COOR = 1

    def __init__(self,
                unique_id,
                plate_number_oddity,
                source_coor,
                destination_coor,
                max_speed,
                car_direction,
                model):
        super().__init__(unique_id,model)
        self.plate_number_oddity = plate_number_oddity # ODD or EVEN
        self.current_coor = source_coor
        self.destination_coor = destination_coor
        self.current_direction = car_direction
        self.max_speed = max_speed

    def neighbors(self):
        neighbors = self.model.grid.neighbor_iter(
                        (self.current_coor[X_COOR],
                        self.current_coor[Y_COOR]), False) # False = only takes Von Neumann neighbours

        return neighbors

    # SimultaneousActivation required two methods: step and advance
    def step(self):
        """ step """
        neighbors = self.neighbors()

        #for neighbor in neighbors:
        #    if neighbor[X_COOR] == self.current_coor[X_COOR]:


    def advance(self):
        """ advance """


class Road(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
