from road_network_model.constant import GRID_HEIGHT, LAYOUT_FILENAME

class MapGenerator:

    def __init__(self, filename = LAYOUT_FILENAME):
        super().__init__()
        layout = open(filename, 'r')
        lines = layout.readlines()

        self.road = []
        self.building = []
        y = GRID_HEIGHT - 1

        for line in lines:
            x = 0
            for i in range(len(line.strip())):
                if(line.strip()[i] == 'X'):
                    self.road.append((x, y))
                if(line.strip()[i] == '@'):
                    self.building.append((x, y))
                x += 1
            y -= 1

    def generate_road_position(self):
        return self.road

    def generate_building_position(self):
        return self.building
