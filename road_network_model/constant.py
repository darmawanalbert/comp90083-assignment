# Project Metadata
PROJECT_TITLE = "Odd-Even Rationing Control"

# HTML Canvas Size
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 1000

# Grid Size
GRID_WIDTH = 100
GRID_HEIGHT = 100

# Initialization Constant
NUMBER_OF_CARS = 1

LAYOUT_FILENAME = "road_network_model/layouts/map2_100x100.layout"

COLOR = {
    "dark_grey":"#333333",
    "light_grey":"#ECECEC"
}

# Directions (based on Von Neumann Neighbour)
# Dictionary of [x,y] vector
DIRECTION = {
    "^": [0,1],
    "v": [0,-1],
    "<": [-1,0],
    ">": [1,0],
    #"_": [0,0]
}

# proportion of office workers for each day
DAY = [1.0, 0.7, 0.8, 0.2, 0.1, 1.0]

# Car State
CAR_STATE = {
    "IDLE": 0,
    "MOVE": 1,
    "FINISHED": 2
}

INTERSECTION = {
    "AVE_AVE": 'T',
    "AVE_ST": 't',
    "ST_AVE": '+',
    "ST_ST": '#',
    "ALL_LA": '*'
}

INTERSECTION_SIGN = ['T','t','+','#','*']

BUILDING = {
    "O": 'OFFICE',
    "R": 'RESIDENCE',
    "E": 'ENTERTAINMENT'
}
