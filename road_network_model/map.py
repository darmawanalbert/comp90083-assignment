from road_network_model.constant import GRID_HEIGHT, LAYOUT_FILENAME, GRID_WIDTH


# Legends
# ^ : North
# v : South
# < : West
# > : East
# @ : Building (nodes)
# - : Nothing


class MapGenerator:

    def __init__(self, filename = LAYOUT_FILENAME):
        super().__init__()
        raw_layout = open(filename, 'r')
        lines = raw_layout.readlines()

        self.road = []
        self.building = []
        self.road_directions = ['<','>','^','v']
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
                if(line.strip()[i] == '@'):
                    self.building.append((x, y))
                
                ## replace # with line.strip()[i]
                self.layout[x][y] = line.strip()[i]
                x += 1
            y -= 1


    def get_road_position(self):
        return self.road

    def get_building_position(self):
        return self.building

    def get_layout(self):
        return self.layout
