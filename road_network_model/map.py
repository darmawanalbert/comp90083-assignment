from road_network_model.constant import GRID_HEIGHT, LAYOUT_FILENAME, GRID_WIDTH, INTERSECTION
import math

# Legends
# Directions
# ^ : North
# v : South
# < : West
# > : East

# Nodes
# O : Office
# R : Residence
# E : Entertaint
# _ : Nothing

# Intersections
# T : Avenue -> Avenue
# t : Avenue -> Street
# + : Street -> Avenue
# # : Street -> Street
# * : All Types -> Lane

class MapGenerator:

    def __init__(self, filename = LAYOUT_FILENAME):
        super().__init__()
        raw_layout = open(filename, 'r')
        lines = raw_layout.readlines()

        self.road = []
        self.offices = []
        self.residences = []
        self.entertaints = []
        self.traffic_light = []
        self.road_directions = ['<','>','^','v','x','t','T','+','#','*']
        self.traffic_light_sign = ['T','t','+','#']
        self.layout = []
        y = GRID_HEIGHT - 1

        ## initialize 2D layout
        for i in range(0, GRID_WIDTH):
            temp = []
            for j in range(0, GRID_HEIGHT):
                temp.append("$")
            self.layout.append(temp)

        ## set road, building, layout
        for line in lines:
            x = 0
            for i in range(len(line.strip())):
                if(line.strip()[i] in self.road_directions):
                    self.road.append((x, y))
                if(line.strip()[i] == 'O'):
                    self.offices.append((x, y))
                if(line.strip()[i] == 'R'):
                    self.residences.append((x, y))
                if(line.strip()[i] == 'E'):
                    self.entertaints.append((x, y))
                if(line.strip()[i] in self.traffic_light_sign):
                    self.traffic_light.append((x, y))

                self.layout[x][y] = line.strip()[i]

                x += 1
            y -= 1


    def get_road_position(self):
        return self.road

    def get_office_position(self):
        return self.offices

    def get_residence_position(self):
        return self.residences

    def get_entertaint_position(self):
        return self.entertaints

    def get_traffic_light_position(self):
        return self.traffic_light

    def get_layout(self):
        return self.layout

    def get_fringes(self, x, y):
        state_fringes = []
        state_fringes.append(((x + 1, y), ">"))
        state_fringes.append(((x - 1, y), "<"))
        state_fringes.append(((x, y + 1), "^"))
        state_fringes.append(((x, y - 1), "v"))

        result_next_state = []
        for state_fringe in state_fringes:
            if self.is_road(state_fringe[0][0], state_fringe[0][1]) == True:
                result_next_state.append(state_fringe)

        return result_next_state

    def is_road(self, x, y):
        coordinate = (x, y)
        if coordinate in self.road:
            return True
        else:
            return False

    def rotate_possible_exit_deltas(self, possible_exit_deltas, previous_direction, intersection_type):
        # No rotation is needed for single lane
        if intersection_type == INTERSECTION["ALL_LA"]:
            return possible_exit_deltas
        # Positive degree is counter-clockwise
        degree = 0
        if (previous_direction == '<'):
            degree = math.pi / 2
        if (previous_direction == 'v'):
            degree = math.pi
        if (previous_direction == '>'):
            degree = 3 * math.pi / 2
        # Apply rotation matrix to all elements inside possible_exit_deltas
        updated_exit_deltas = []
        for possible_exit_delta in possible_exit_deltas:
            current_x = possible_exit_delta[0]
            current_y = possible_exit_delta[1]
            x = (current_x * int(math.cos(degree))) - (current_y * int(math.sin(degree)))
            y = (current_x * int(math.sin(degree))) + (current_y * int(math.cos(degree)))
            updated_exit_deltas.append((x,y))
        return updated_exit_deltas

    def get_exit_point(self, current_pos, previous_direction, intersection_type):
        exit_points = []
        current_x = current_pos[0]
        current_y = current_pos[1]
        number_of_fringes = len(self.get_fringes(current_x, current_y))

        if(intersection_type == INTERSECTION["AVE_AVE"]):
            if number_of_fringes == 4: # Inner Lane
                # 4 possibilities for each previous_direction:
                # 1. Turn left, take right lane
                # 2. Turn right, take left lane
                # 3. Turn right, take right lane
                # 4. Go straight
                possible_exit_deltas = [(-2, 2), (3, 4), (3, 3), (0, 5)]
            else: # Outer Lane
                # 4 possibilities for each previous_direction:
                # 1. Turn left, take left lane
                # 2. Turn right, take left lane
                # 3. Turn right, take right lane
                # 4. Go straight
                possible_exit_deltas = [(-1, 1), (4, 4), (4, 3), (0, 5)]
        elif(intersection_type == INTERSECTION["AVE_ST"]):
            if number_of_fringes == 4: # Inner Lane
                # 3 possibilities for each previous_direction: turn left, turn right, or go straight
                possible_exit_deltas = [(-2, 1), (3, 2), (0, 3)]
            else: # Outer Lane
                # 3 possibilities for each previous_direction: turn left, turn right, or go straight
                possible_exit_deltas = [(-1, 1), (4, 2), (0, 3)]
        elif(intersection_type == INTERSECTION["ST_ST"]):
            # 3 possibilities for each previous_direction: turn left, turn right, or go straight
            possible_exit_deltas = [(-1, 1), (2, 2), (0, 3)]
        elif(intersection_type == INTERSECTION["ST_AVE"]):
            # 5 possibilities for each previous_direction:
            # 1. Turn left, take left lane
            # 2. Turn left, take right lane
            # 3. Turn right, take left lane
            # 4. Turn right, take right lane
            # 5. Go straight
            possible_exit_deltas = [(-1, 1), (-1, 2), (2, 4), (2, 3), (0, 5)]
        elif(intersection_type == INTERSECTION["ALL_LA"]):
            possible_exit_deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        else:
            possible_exit_deltas = []
        # Defensive programming: Check whether the given previous_direction is one of four possible directions
        rotated_possible_exit_deltas = self.rotate_possible_exit_deltas(possible_exit_deltas, previous_direction, intersection_type)
        for possible_exit_delta in rotated_possible_exit_deltas:
            delta_x = possible_exit_delta[0]
            delta_y = possible_exit_delta[1]
            x = current_x + delta_x
            y = current_y + delta_y
            if x >= 0 and y >= 0 and x < GRID_WIDTH and y < GRID_HEIGHT:
                if (self.is_road(x, y)):
                    exit_points.append(((x, y), self.layout[x][y]))

        return exit_points
