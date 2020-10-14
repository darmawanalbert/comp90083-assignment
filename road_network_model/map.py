from road_network_model.constant import GRID_HEIGHT, LAYOUT_FILENAME, GRID_WIDTH


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
        self.road_directions = ['<','>','^','v','+']
        self.layout = []
        y = GRID_HEIGHT - 1

        ## initialize 2D layout
        for i in range(0, GRID_WIDTH):
            temp = []
            for j in range(0, GRID_HEIGHT):
                temp.append("#")
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

        print("x: ", x, ", y: ", y)
        
        state_fringes = []
        state_fringes.append(((x + 1, y), ">"))
        state_fringes.append(((x - 1, y), "<"))
        state_fringes.append(((x, y + 1), "^"))
        state_fringes.append(((x, y - 1), "v"))
        
        print("state_fringes: ", state_fringes)

        result_next_state = []
        for state_fringe in state_fringes:
            if self.is_road(state_fringe[0][0], state_fringe[0][1]) == True:
                result_next_state.append(state_fringe)

        print("result_next_state: ", result_next_state)
        
        return result_next_state

    def is_road(self, x, y):
        coordinate = (x, y)
        if coordinate in self.road:
            return True
        else:
            return False