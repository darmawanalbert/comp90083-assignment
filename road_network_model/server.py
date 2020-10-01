from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from road_network_model.agent import Car
from road_network_model.model import RoadNetworkModel
from road_network_model.portrayal import road_network_model_portrayal
from road_network_model.constant import PROJECT_TITLE, CANVAS_WIDTH, CANVAS_HEIGHT, GRID_WIDTH, GRID_HEIGHT, NUMBER_OF_CARS

# Define a CanvasGrid to visualise the Road Network Model
canvas_element = CanvasGrid(road_network_model_portrayal, GRID_WIDTH, GRID_HEIGHT, CANVAS_WIDTH, CANVAS_HEIGHT)

# Define parameter of Road Network Model
road_network_model_params = {
    "number_of_cars": NUMBER_OF_CARS,
    "width": GRID_WIDTH,
    "height": GRID_HEIGHT
}

# Instantiate the server at port 8521
server = ModularServer(
    RoadNetworkModel, [canvas_element], PROJECT_TITLE, road_network_model_params
)

server.port = 8521
