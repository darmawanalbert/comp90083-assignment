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
                departure_time,
                return_time,
                activity_level,
                model):
        super().__init__(unique_id,model)
        self.plate_number_oddity = plate_number_oddity # ODD or EVEN, 0 is even and 1 is odd
        self.current_coor = source_coor
        self.source_coor = source_coor
        self.destination_coor = destination_coor
        self.exit_direction = car_direction
        self.absolute_source_coor = source_coor
        self.current_direction = car_direction
        self.current_state = car_state # initialised to be 'IDLE'
        self.next_coor = (0,0)
        self.departure_time = departure_time
        self.return_time = return_time
        self.next_state = None
        self.shortest_exit_point = None
        self.travel_time = 0
        self.front_coor = None
        self.arrive_at_destination = 0
        self.activity_level = activity_level

    def neighbors(self):
        neighbors = self.model.grid.neighbor_iter(
                        (self.current_coor[Car.X_COOR],
                        self.current_coor[Car.Y_COOR]), # False = only takes Von Neumann neighbours
                        True) # True = includes centre

        return neighbors

    # SimultaneousActivation required two methods: step and advance
    def step(self):
        # STATE:
        # IDLE <-> MOVE <-> FINISHED

        # Map Information
        map_instance = self.model.map
        layout = map_instance.get_layout()

        # if it's time for car to depart
        if self.current_state == "IDLE":
            # IDLE -> MOVE
            if self.front_coor != None: # checks traffic jam
                # Get neighbours
                neighbors = self.neighbors()
                car_in_front = False

                for neighbor in neighbors:
                    if (isinstance(neighbor, Car)
                        and neighbor.current_coor == self.front_coor):
                        # Check whether the neighbour car is in front
                        car_in_front = True

                if not car_in_front:
                    self.front_coor == None

            if (self.model.tick >= self.departure_time
                and self.front_coor == None):
                self.current_state = "MOVE"

        # if self.current_state is finished, check if it's time to return
        if self.current_state == "FINISHED":
            if ((self.activity_level == "PEAK_HOURS" and self.arrive_at_destination < 2)
            or self.activity_level == "HIGHLY_ACTIVE"
            or (self.activity_level == "BUSINESS_HOURS"
                and (self.current_coor != self.absolute_source_coor
                or self.return_time <= self.model.end_peak_hour_2))):
                # cars that are not home must return or if it's home, do not leave when it's after peak hour 2
                if self.model.tick >= self.return_time:
                    self.current_state = "MOVE"

        # performs "MOVE" procedure
        if self.current_state == "MOVE":
            # Get neighbours
            neighbors = self.neighbors()

            # Get new_direction
            new_direction = layout[self.current_coor[0]][self.current_coor[1]]

            # Get current coor, to be updated
            new_x = self.current_coor[0]
            new_y = self.current_coor[1]

            updated_direction = ""
            # Determine Car direction
            # Inside a Office / Residence / Entertainment
            if (self.current_coor[0] == self.destination_coor[0]
                and (abs(self.current_coor[1] - self.destination_coor[1]) <= 4)
                and (abs(self.current_coor[1] - self.destination_coor[1]) > 0)
                and map_instance.is_all_road(1, self.current_coor, self.destination_coor)):

                diff = self.current_coor[1] - self.destination_coor[1]
                flag = True

                for i in range(abs(diff)):
                    if (diff < 0):
                        enter_direction = "^"
                        current_y = self.current_coor[1] + i
                    else:
                        enter_direction = "v"
                        current_y = self.destination_coor[1] + i

                if flag:
                    updated_direction = enter_direction

            elif (self.current_coor[1] == self.destination_coor[1]
                and (abs(self.current_coor[0] - self.destination_coor[0]) <= 4)
                and (abs(self.current_coor[0] - self.destination_coor[0]) > 0)
                and map_instance.is_all_road(0, self.current_coor, self.destination_coor)
                ):

                diff = self.current_coor[0] - self.destination_coor[0]
                flag = True

                for i in range(abs(diff)):
                    if (diff < 0):
                        enter_direction = ">"
                        current_x = self.current_coor[0] + i
                    else:
                        enter_direction = "<"
                        current_x = self.destination_coor[0] + i

                if flag:
                    updated_direction = enter_direction

            # Car is in building
            elif new_direction in BUILDING:
                updated_direction = self.exit_direction
                self.current_direction = updated_direction

            # Encounter an intersection
            elif new_direction in INTERSECTION_SIGN:
                current_pos = (self.current_coor[0], self.current_coor[1])
                intersection_type = layout[self.current_coor[0]][self.current_coor[1]]
                exit_points = map_instance.get_exit_point(current_pos, self.current_direction, intersection_type)
                shortest_distance = float("inf")
                shortest_exit_point = ()
                for exit_point in exit_points:
                    if self.model.is_odd_even_policy_enabled == True and self.model.is_odd_even_policy_time() == True:
                        if self.model.is_plate_number_oddity_allowed(self.plate_number_oddity, exit_point[0]) == True:
                            newDist = get_euclidean_distance(exit_point[0], self.destination_coor)
                            if newDist < shortest_distance:
                                shortest_distance = newDist
                                shortest_exit_point = exit_point[0]
                        # else
                        # is an avenue (i.e. not allowed to pass due to odd/even), do not append
                    else:
                        newDist = get_euclidean_distance(exit_point[0], self.destination_coor)
                        if newDist < shortest_distance:
                            shortest_distance = newDist
                            shortest_exit_point = exit_point[0]


                self.shortest_exit_point = shortest_exit_point

                local_current_direction = get_next_direction(self.current_direction, self.current_coor, layout[self.shortest_exit_point[0]][self.shortest_exit_point[1]], self.shortest_exit_point)
                updated_direction = local_current_direction

            # Inside an Intersection
            elif new_direction == "x":
                local_current_direction = get_next_direction(self.current_direction, self.current_coor, layout[self.shortest_exit_point[0]][self.shortest_exit_point[1]], self.shortest_exit_point)
                updated_direction = local_current_direction

            else: # On a road, only one way to go
                self.current_direction = new_direction
                updated_direction = new_direction

            # updating new_x and new_y
            new_x = self.current_coor[0] + DIRECTION[updated_direction][0]
            new_y = self.current_coor[1] + DIRECTION[updated_direction][1]
            if new_x < 0 or new_x >= GRID_WIDTH:
                new_x = self.current_coor[0]
            if new_y < 0 or new_y >= GRID_HEIGHT:
                new_y = self.current_coor[1]

            self.next_coor = (new_x, new_y)

            car_in_front = False
            front_neighbor = None
            for neighbor in neighbors:
                if isinstance(neighbor, Car):
                    # Check whether the neighbour car is in front
                    if neighbor.current_coor == (new_x, new_y):
                        car_in_front = True
                        front_neighbor = neighbor
                        self.front_coor = (new_x, new_y)

            # MOVE -> IDLE
            if car_in_front:
                if front_neighbor.current_state == "IDLE":
                    self.current_state = "IDLE"
                else:
                    self.next_coor = (new_x, new_y)
            else:
                self.next_coor = (new_x, new_y)

            # if travelling, add mean travel time
            if self.current_state == "MOVE":
                self.travel_time += 1
            else:
                self.travel_time += 0

            # if next_coor is destination, state is finished
            # MOVE -> FINISHED
            if self.current_state != "IDLE":
                if self.next_coor == self.destination_coor:
                    self.current_state = "FINISHED"
                    self.arrive_at_destination += 1
                    # Now, destination is to return home
                    destination_coor_temp = self.destination_coor
                    self.destination_coor = self.source_coor
                    self.source_coor = destination_coor_temp

                    # Return soon if activity is HIGHLY_ACTIVE or BUSINESS_HOURS
                    if self.activity_level == "HIGHLY_ACTIVE" or self.activity_level == "BUSINESS_HOURS":
                        self.return_time = self.model.tick + 5

                    state_fringes = map_instance.get_fringes(self.next_coor[0], self.next_coor[1])
                    shortest_distance = float("inf")
                    car_direction = state_fringes[0][1]
                    for state_fringe in state_fringes:
                        current_direction =  state_fringe[1] # "^" "v" ">" "<"
                        if current_direction in DIRECTION:
                            temp_x = state_fringe[0][0] + DIRECTION[current_direction][0]
                            temp_y = state_fringe[0][1] + DIRECTION[current_direction][1]

                            newDist = get_euclidean_distance((temp_x, temp_y), (self.destination_coor[0], self.destination_coor[1]))
                            if newDist < shortest_distance:
                                shortest_distance = newDist
                                car_direction = current_direction
                    self.exit_direction = car_direction
                else:
                    pass

        else: # stay put when current_state is "IDLE" or "FINISHED"
            self.next_coor = self.current_coor

    def advance(self):
        self.current_coor = self.next_coor
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

class Entertainment(Agent):
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

    def advance(self):
        self.current_coor = self.next_coor
        self.model.grid.move_agent(self, self.next_coor)
