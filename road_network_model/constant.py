# Project Metadata
PROJECT_TITLE = "Odd-Even Rationing Control"

# HTML Canvas Size
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 1000

# Grid Size
GRID_WIDTH = 100
GRID_HEIGHT = 100

# Initialization Constant
NUMBER_OF_CARS = 30

LAYOUT_FILENAME = "road_network_model/layouts/map_100x100.layout"

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
DAY = [0.60, 0.65, 0.60, 0.40, 0.35, 0.60]

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

ACTIVITY = ["HIGHLY_ACTIVE", "BUSINESS_HOURS", "PEAK_HOURS"]

# Peak Hours
PEAK_HOURS = {
    "START_PEAK_HOUR_1" : 420,
    "END_PEAK_HOUR_1" : 600,
    "START_PEAK_HOUR_2" : 960,
    "END_PEAK_HOUR_2" : 1140
}

ACTIVITY_PROPORTION = {
    "HIGHLY_ACTIVE" : 0.05,
    "BUSINESS_HOURS" : 0.27,
    "PEAK_HOURS" : 0.68
}