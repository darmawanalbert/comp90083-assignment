from road_network_model.constant import GRID_HEIGHT, LAYOUT_FILENAME, GRID_WIDTH, INTERSECTION

# Legends
# ^ : North
# v : South
# < : West
# > : East
# + : intersections
# O : Office (nodes)
# R : Residence (nodes)
# E : Entertaint (nodes)
# - : Nothing


class MapGenerator:

    def __init__(self, filename = LAYOUT_FILENAME):
        super().__init__()
        raw_layout = open(filename, 'r')
        lines = raw_layout.readlines()

        self.road = []
        self.offices = []
        self.residences = []
        self.entertaints = []
        self.road_directions = ['<','>','^','v','+','x','t','T','+','#','*']
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

    def get_layout(self):
        return self.layout
    
    def get_successors(self, x, y):

        #print("x: ", x, ", y: ", y)
        
        state_fringes = []
        state_fringes.append(((x + 1, y), ">"))
        state_fringes.append(((x - 1, y), "<"))
        state_fringes.append(((x, y + 1), "^"))
        state_fringes.append(((x, y - 1), "v"))
        
        #print("state_fringes: ", state_fringes)

        result_next_state = []
        for state_fringe in state_fringes:
            if self.is_road(state_fringe[0][0], state_fringe[0][1]) == True:
                result_next_state.append(state_fringe)

        #print("result_next_state: ", result_next_state)
        
        return result_next_state

    def is_road(self, x, y):
        coordinate = (x, y)
        if coordinate in self.road:
            return True
        else:
            return False
    
    def get_exit_point(self, current_pos, previous_direction, intersection_type):
        print("current_pos: ", current_pos, ", previous_direction: ", previous_direction, ", intersection_type: ", intersection_type)
        exit_point = []
        if(intersection_type == INTERSECTION["AVE_AVE"]): ## AxA
            exit_point = self.avenue_x_avenue(current_pos, previous_direction)
        elif(intersection_type == INTERSECTION["AVE_ST"]): ## AxS
            exit_point = self.avenue_x_street(current_pos, previous_direction)
        elif(intersection_type == INTERSECTION["ST_ST"]): ## SxS
            exit_point = self.street_x_street(current_pos, previous_direction)
        elif(intersection_type == INTERSECTION["ST_AVE"]): ## SxA
            exit_point = self.street_x_avenue(current_pos, previous_direction)
        elif(intersection_type == INTERSECTION["ALL_LA"]): ## all type x Lane
            exit_point = self.all_x_lane(current_pos, previous_direction)
        else:
            print("unknown intersection type")
        
        print("exit_point: ", exit_point)
        return exit_point
    
    def avenue_x_avenue(self, current_pos, previous_direction):
        temp_exit_point = []
        curr_x = current_pos[0]
        curr_y = current_pos[1]
        if(previous_direction == '^'):
            if(len(self.get_successors(curr_x, curr_y)) == 4):
                temp_exit_point.append(((curr_x - 2, curr_y - 1), self.layout[curr_x - 2][curr_y - 1])) # left, left lane
                temp_exit_point.append(((curr_x - 2, curr_y - 2), self.layout[curr_x - 2][curr_y - 2])) # left, right lane
                
                temp_exit_point.append(((curr_x + 3, curr_y - 3), self.layout[curr_x + 3][curr_y - 3])) # right, left lane
                temp_exit_point.append(((curr_x + 3, curr_y - 4), self.layout[curr_x + 3][curr_y - 4])) # right, right lane
                
                temp_exit_point.append(((curr_x, curr_y - 4), self.layout[curr_x][curr_y - 4])) # straight,
            else:
                temp_exit_point.append(((curr_x - 1, curr_y - 1), self.layout[curr_x - 1][curr_y - 1])) # left, left lane
                temp_exit_point.append(((curr_x - 1, curr_y - 2), self.layout[curr_x - 1][curr_y - 2])) # left, right lane
                
                temp_exit_point.append(((curr_x + 4, curr_y - 3), self.layout[curr_x + 4][curr_y - 3])) # right, left lane
                temp_exit_point.append(((curr_x + 4, curr_y - 4), self.layout[curr_x + 4][curr_y - 4])) # right, right lane
                
                temp_exit_point.append(((curr_x, curr_y - 4), self.layout[curr_x][curr_y - 4])) # straight,
            
        elif(previous_direction == '>'):
            if(len(self.get_successors(curr_x, curr_y)) == 4):
                temp_exit_point.append(((curr_x + 1, curr_y + 2), self.layout[curr_x + 1][curr_y + 2])) # left, left lane
                temp_exit_point.append(((curr_x + 2, curr_y + 2), self.layout[curr_x + 2][curr_y + 2])) # left, right lane
                
                temp_exit_point.append(((curr_x + 3, curr_y - 3), self.layout[curr_x + 3][curr_y - 3])) # right, left lane
                temp_exit_point.append(((curr_x + 4, curr_y - 3), self.layout[curr_x + 4][curr_y - 3])) # right, right lane
                
                temp_exit_point.append(((curr_x + 5, curr_y), self.layout[curr_x + 5][curr_y])) # straight,
            else:
                temp_exit_point.append(((curr_x + 1, curr_y + 1), self.layout[curr_x + 1][curr_y + 1])) # left, left lane
                temp_exit_point.append(((curr_x + 2, curr_y + 1), self.layout[curr_x + 2][curr_y + 1])) # left, right lane
                
                temp_exit_point.append(((curr_x + 3, curr_y - 4), self.layout[curr_x + 3][curr_y - 4])) # right, left lane
                temp_exit_point.append(((curr_x + 4, curr_y - 4), self.layout[curr_x + 4][curr_y - 4])) # right, right lane
                
                temp_exit_point.append(((curr_x + 5, curr_y), self.layout[curr_x + 5][curr_y])) # straight,

        elif(previous_direction == 'v'):
            if(len(self.get_successors(curr_x, curr_y)) == 4):
                temp_exit_point.append(((curr_x + 2, curr_y + 1), self.layout[curr_x + 2][curr_y + 1])) # left, left lane
                temp_exit_point.append(((curr_x + 2, curr_y + 2), self.layout[curr_x + 2][curr_y + 2])) # left, right lane
                
                temp_exit_point.append(((curr_x - 3, curr_y + 3), self.layout[curr_x - 3][curr_y + 3])) # right, left lane
                temp_exit_point.append(((curr_x - 3, curr_y + 4), self.layout[curr_x - 3][curr_y + 4])) # right, right lane
                
                temp_exit_point.append((curr_x, curr_y + 4), self.layout[curr_x][curr_y + 4]) # straight,
            else:
                temp_exit_point.append(((curr_x + 1, curr_y + 1), self.layout[curr_x + 2][curr_y + 1])) # left, left lane
                temp_exit_point.append(((curr_x + 1, curr_y + 2), self.layout[curr_x + 2][curr_y + 2])) # left, right lane
                
                temp_exit_point.append(((curr_x - 4, curr_y + 3), self.layout[curr_x - 3][curr_y + 3])) # right, left lane
                temp_exit_point.append(((curr_x - 4, curr_y + 4), self.layout[curr_x - 3][curr_y + 4])) # right, right lane
                
                temp_exit_point.append(((curr_x, curr_y + 4), self.layout[curr_x][curr_y + 4])) # straight,
            
        elif(previous_direction == '<'):
            if(len(self.get_successors(curr_x, curr_y)) == 4):
                temp_exit_point.append(((curr_x - 1, curr_y + 2), self.layout[curr_x - 1][curr_y + 2])) # left, left lane
                temp_exit_point.append(((curr_x - 2, curr_y + 2), self.layout[curr_x - 2][curr_y + 2])) # left, right lane
                
                temp_exit_point.append(((curr_x - 1, curr_y - 3), self.layout[curr_x - 1][curr_y - 3])) # right, left lane
                temp_exit_point.append(((curr_x - 2, curr_y - 3), self.layout[curr_x - 2][curr_y - 3])) # right, right lane
                
                temp_exit_point.append(((curr_x - 4, curr_y), self.layout[curr_x - 4][curr_y])) # straight,
            else:
                temp_exit_point.append(((curr_x - 1, curr_y + 1), self.layout[curr_x - 1][curr_y + 1])) # left, left lane
                temp_exit_point.append(((curr_x - 2, curr_y + 1), self.layout[curr_x - 2][curr_y + 1])) # left, right lane
                
                temp_exit_point.append(((curr_x - 3, curr_y - 3), self.layout[curr_x - 3][curr_y - 3])) # right, left lane
                temp_exit_point.append(((curr_x - 4, curr_y - 3), self.layout[curr_x - 4][curr_y - 3])) # right, right lane
                
                temp_exit_point.append(((curr_x - 4, curr_y), self.layout[curr_x - 4][curr_y])) # straight,
            
        else:
            print("unknown direction!")

        exit_point = []
        for ep in temp_exit_point:
            state = ep[0]
            if(self.is_road(state[0], state[1])):
                exit_point.append(ep)

        return exit_point
        
    def avenue_x_street(self, current_pos, previous_direction):
        exit_point = []
        curr_x = current_pos[0]
        curr_y = current_pos[1]

        car_on_first_lane = False
        if len(self.get_successors(current_pos[0], current_pos[1])) == 3:
            car_on_first_lane = True
        elif len(self.get_successors(current_pos[0], current_pos[1])) == 4:
            car_on_first_lane = False
        else:
            print("Error! Car is neither on the first nor second lane.")
            return exit_point

        if(previous_direction == '^'):
            # left exit point
            if (car_on_first_lane):
                point1 = (curr_x - 1, curr_y - 1)
                left_from_lane1 = (point1, self.layout[point1[0]][point1[1]])
                if self.is_road(point1[0], point1[1]):
                    exit_point.append(left_from_lane1)
            else:
                point2 = (curr_x -2, curr_y - 2)
                left_from_lane2 = (point2, self.layout[point2[0]][point2[1]])
                if self.is_road(point2[0], point2[1]):
                    exit_point.append(left_from_lane2)

            # right exit point
            if (car_on_first_lane):
                point1 = (curr_x + 4, curr_y - 2)
                right_from_lane1 = (point1, self.layout[point1[0]][point1[1]])
                if self.is_road(point1[0], point1[1]):
                    exit_point.append(right_from_lane1)
            else:
                point2 = (curr_x + 3, curr_y - 2)
                right_from_lane2 = (point2, self.layout[point2[0]][point2[1]])
                if self.is_road(point2[0], point2[1]):
                    exit_point.append(right_from_lane2)
            
            # straight exit point
            point = (curr_x + 0, curr_y - 3)
            straight = (point, self.layout[point[0]][point[1]])
            if self.is_road(point[0], point[1]):
                exit_point.append(straight)
            
        elif(previous_direction == '>'):
            # left exit point
            if (car_on_first_lane):
                point1=(curr_x + 1, curr_y - 1)
                left_from_lane1=(point1, self.layout[point1[0]][point1[1]])
                if self.is_road(point1[0], point1[1]):
                    exit_point.append(left_from_lane1)
            else:
                point2=(curr_x + 1, curr_y - 2)
                left_from_lane2=(point2, self.layout[point2[0]][point2[1]])
                if self.is_road(point2[0], point2[1]):
                    exit_point.append(left_from_lane2)

            # right exit point
            if (car_on_first_lane):
                point1 = (curr_x + 2, curr_y - 4)
                right_from_lane1 = (point1, self.layout[point1[0]][point1[1]])
                if self.is_road(point1[0], point1[1]):
                    exit_point.append(right_from_lane1)
            else:
                point2 = (curr_x + 2, curr_y - 3)
                right_from_lane2 = (point2, self.layout[point2[0]][point2[1]])
                if self.is_road(point2[0], point2[1]):
                    exit_point.append(right_from_lane2)

            # straight exit point
            point = (curr_x + 3, curr_y + 0)
            straight = (point, self.layout[point[0][point[1]]])
            if self.is_road(point2[0], point2[1]):
                exit_point.append(straight)

        elif(previous_direction == 'v'):
            # left exit point
            if (car_on_first_lane):
                point1 = (curr_x + 1, curr_y + 1)
                left_from_lane1 = (point1, self.layout[point1[0]][point1[1]])
                if self.is_road(point1[0], point1[1]):
                    exit_point.append(left_from_lane1)
            else:
                point2 = (curr_x + 2, curr_y + 1)
                left_from_lane2 = (point2, self.layout[point2[0]][point2[1]])
                if self.is_road(point2[0], point2[1]):
                    exit_point.append(left_from_lane2)

            # right exit point
            if (car_on_first_lane):
                point1 = (curr_x - 4, curr_y + 2)
                right_from_lane1 = (point1, self.layout[point1[0]][point1[1]])
                if self.is_road(point1[0], point1[1]):
                    exit_point.append(right_from_lane1)
            else:
                point2 = (curr_x - 3, curr_y + 2)
                right_from_lane2 = (point2, self.layout[point2[0]][point2[1]])
                if self.is_road(point2[0], point2[1]):
                    exit_point.append(right_from_lane2)

            # straight exit point
            point = (curr_x + 0, curr_y + 3)
            straight = (point, self.layout[point[0][point[1]]])
            if self.is_road(point2[0], point2[1]):
                exit_point.append(straight)

        elif(previous_direction == '<'):
            # left exit point
            if (car_on_first_lane):
                point1 = (curr_x - 1, curr_y + 1)
                left_from_lane1 = (point1, self.layout[point1[0]][point1[1]])
                if self.is_road(point1[0], point1[1]):
                    exit_point.append(left_from_lane1)
            else:
                point2 = (curr_x - 1, curr_y + 2)
                left_from_lane2 = (point2, self.layout[point2[0]][point2[1]])
                if self.is_road(point2[0], point2[1]):
                    exit_point.append(left_from_lane2)

            # right exit point
            if (car_on_first_lane):
                point1 = (curr_x - 2, curr_y + 4)
                right_from_lane1 = (point1, self.layout[point1[0]][point1[1]])
                if self.is_road(point1[0], point1[1]):
                    exit_point.append(right_from_lane1)
            else:
                point2 = (curr_x - 2, curr_y + 3)
                right_from_lane2 = (point2, self.layout[point2[0]][point2[1]])
                if self.is_road(point2[0], point2[1]):
                    exit_point.append(right_from_lane2)

            # straight exit point
            point = (curr_x - 3, curr_y + 0)
            straight = (point, self.layout[point[0][point[1]]])
            if self.is_road(point2[0], point2[1]):
                exit_point.append(straight)

        else:
            print("unknown direction!")
        
        
        if (len(exit_point) == 0):
            print("Invalid intersection! Zero exit points.")
        
        return exit_point

    def street_x_street(self, current_pos, previous_direction):
        exit_point = []
        curr_x = current_pos[0]
        curr_y = current_pos[1]

        if(previous_direction == '^'):
            # left exit point
            point = (curr_x - 1, curr_y - 1)
            left = (point, self.layout[point[0][point[1]]])
            if (self.is_road(point[0], point[1])):
                exit_point.append(left)
            
            # right exit point
            point = (curr_x + 2, curr_y - 2)
            right = (point, self.layout[point[0][point[1]]])
            if (self.is_road(point[0], point[1])):
                exit_point.append(right)

            # straight exit point
            point = (curr_x + 0, curr_y - 3)
            straight = (point, self.layout[point[0][point[1]]])
            if (self.is_road(point[0], point[1])):
                exit_point.append(straight)

        elif(previous_direction == '>'):
            # left exit point
            point = (curr_x + 1, curr_y - 1)
            left = (point, self.layout[point[0][point[1]]])
            if (self.is_road(point[0], point[1])):
                exit_point.append(left)

            # right exit point
            point = (curr_x + 2, curr_y + 2)
            right = (point, self.layout[point[0][point[1]]])
            if (self.is_road(point[0], point[1])):
                exit_point.append(right)

            # straight exit point
            point = (curr_x + 3, curr_y + 0)
            straight = (point, self.layout[point[0][point[1]]])
            if (self.is_road(point[0], point[1])):
                exit_point.append(straight)

        elif(previous_direction == 'v'):
            # left exit point
            point = (curr_x + 1, curr_y + 1)
            left = (point, self.layout[point[0][point[1]]])
            if (self.is_road(point[0], point[1])):
                exit_point.append(left)

            # right exit point
            point = (curr_x - 2, curr_y + 2)
            right = (point, self.layout[point[0][point[1]]])
            if (self.is_road(point[0], point[1])):
                exit_point.append(right)

            # straight exit point
            point = (curr_x + 0, curr_y + 3)
            straight = (point, self.layout[point[0][point[1]]])
            if (self.is_road(point[0], point[1])):
                exit_point.append(straight)

        elif(previous_direction == '<'):
            # left exit point
            point = (curr_x - 1, curr_y - 1)
            left = (point, self.layout[point[0][point[1]]])
            if (self.is_road(point[0], point[1])):
                exit_point.append(left)

            # right exit point
            point = (curr_x - 2, curr_y + 2)
            right = (point, self.layout[point[0][point[1]]])
            if (self.is_road(point[0], point[1])):
                exit_point.append(right)

            # straight exit point
            point = (curr_x - 3, curr_y + 0)
            straight = (point, self.layout[point[0][point[1]]])
            if (self.is_road(point[0], point[1])):
                exit_point.append(straight)

        else:
            print("unknown direction!")

        if (len(exit_point) == 0):
            print("Invalid intersection! Zero exit points.")

        return exit_point

    def street_x_avenue(self, current_pos, previous_direction):
        temp_exit_point = []
        curr_x = current_pos[0]
        curr_y = current_pos[1]
        if(previous_direction == '^'):
            temp_exit_point.append(((curr_x - 1, curr_y - 1), self.layout[curr_x - 1][curr_y - 1])) # left, left lane
            temp_exit_point.append(((curr_x - 1, curr_y - 2), self.layout[curr_x - 1][curr_y - 2])) # left, right lane
                
            temp_exit_point.append(((curr_x + 1, curr_y - 3), self.layout[curr_x + 1][curr_y - 3])) # right, left lane
            temp_exit_point.append(((curr_x + 1, curr_y - 4), self.layout[curr_x + 1][curr_y - 4])) # right, right lane
                
            temp_exit_point.append(((curr_x, curr_y - 4), self.layout[curr_x][curr_y - 4])) # straight,
            
        elif(previous_direction == '>'):
            temp_exit_point.append(((curr_x + 3, curr_y - 1), self.layout[curr_x - 3][curr_y - 1])) # left, left lane
            temp_exit_point.append(((curr_x + 4, curr_y - 1), self.layout[curr_x - 4][curr_y - 1])) # left, right lane
                
            temp_exit_point.append(((curr_x + 3, curr_y + 1), self.layout[curr_x + 3][curr_y + 1])) # right, left lane
            temp_exit_point.append(((curr_x + 4, curr_y + 1), self.layout[curr_x + 4][curr_y + 1])) # right, right lane
                
            temp_exit_point.append((curr_x + 4, curr_y), self.layout[curr_x + 4][curr_y]) # straight,
            
        elif(previous_direction == 'v'):
            temp_exit_point.append(((curr_x + 1, curr_y + 1), self.layout[curr_x + 1][curr_y + 1])) # left, left lane
            temp_exit_point.append(((curr_x + 1, curr_y + 2), self.layout[curr_x + 1][curr_y + 2])) # left, right lane
                
            temp_exit_point.append(((curr_x - 1, curr_y + 3), self.layout[curr_x - 1][curr_y + 3])) # right, left lane
            temp_exit_point.append(((curr_x - 1, curr_y + 4), self.layout[curr_x - 1][curr_y + 4])) # right, right lane
                
            temp_exit_point.append(((curr_x, curr_y + 4), self.layout[curr_x][curr_y + 4])) # straight,
            
        elif(previous_direction == '<'):
            temp_exit_point.append(((curr_x - 1, curr_y + 1), self.layout[curr_x - 1][curr_y + 1])) # left, left lane
            temp_exit_point.append(((curr_x - 2, curr_y + 1), self.layout[curr_x - 2][curr_y + 1])) # left, right lane
                
            temp_exit_point.append(((curr_x - 1, curr_y - 1), self.layout[curr_x - 1][curr_y - 1])) # right, left lane
            temp_exit_point.append(((curr_x - 2, curr_y - 1), self.layout[curr_x - 2][curr_y - 1])) # right, right lane
                
            temp_exit_point.append(((curr_x - 4, curr_y), self.layout[curr_x - 4][curr_y])) # straight,
            
        else:
            print("unknown direction!")

        exit_point = []
        for ep in temp_exit_point:
            state = ep[0]
            if(self.is_road(state[0], state[1])):
                exit_point.append(ep)

        return exit_point
    
    def all_x_lane(self, current_pos, previous_direction):
        temp_exit_point = []
        curr_x = current_pos[0]
        curr_y = current_pos[1]
        temp_exit_point.append(((curr_x + 1, curr_y), ">"))
        temp_exit_point.append(((curr_x - 1, curr_y), "<"))
        temp_exit_point.append(((curr_x, curr_y + 1), "^"))
        temp_exit_point.append(((curr_x, curr_y - 1), "v"))

        exit_point = []
        for ep in temp_exit_point:
            state = ep[0]
            if(self.is_road(state[0], state[1])):
                exit_point.append(ep)

        return exit_point
        
