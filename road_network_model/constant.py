# Project Metadata
PROJECT_TITLE = "Odd-Even Rationing Control"

# HTML Canvas Size
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400

# Grid Size
GRID_WIDTH = 100
GRID_HEIGHT = 100

# Initialization Constant
NUMBER_OF_CARS = 5

LAYOUT_FILENAME = "road_network_model/layouts/map2_100x100.layout"

# Directions (based on Von Neumann Neighbour)
# Dictionary of [x,y] vector
DIRECTION = {
    "^": [0,1],
    "v": [0,-1],
    "<": [-1,0],
    ">": [1,0],
    "_": [0,0]
}

# Car State
CAR_STATE = {
    "IDLE": 0,
    "MOVE": 1,
    "FINISHED": 2
}
