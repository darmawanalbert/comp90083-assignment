from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import TextElement


from road_network_model.agent import Car, TrafficLight
from road_network_model.model import RoadNetworkModel
from road_network_model.portrayal import road_network_model_portrayal
from road_network_model.constant import PROJECT_TITLE, CANVAS_WIDTH, CANVAS_HEIGHT, GRID_WIDTH, GRID_HEIGHT, NUMBER_OF_CARS

# Define a CanvasGrid to visualise the Road Network Model
canvas_element = CanvasGrid(road_network_model_portrayal, GRID_WIDTH, GRID_HEIGHT, CANVAS_WIDTH, CANVAS_HEIGHT)

class InfoTextElement(TextElement):
    def render(self, model):
        mean_travel_time = model.mean_travel_time
        mean_travel_time_text = "{0:.2f}".format(mean_travel_time)
        day_text = str(model.day)
        oddity_text = ""
        if model.is_odd_date:
            oddity_text = "Odd day"
        else:
            oddity_text = "Even day"
        return "Mean Travel Time: {}<br>Day: {}<br>Oddity: {}".format(mean_travel_time_text, day_text, oddity_text)

# Define parameter of Road Network Model
road_network_model_params = {
    "number_of_cars": NUMBER_OF_CARS,
    "width": GRID_WIDTH,
    "height": GRID_HEIGHT,
    "is_odd_even_policy_enabled": UserSettableParameter("checkbox", "Odd-Even Policy Enabled", True),
}

# Instantiate the server at port 8521
server = ModularServer(
    RoadNetworkModel, [InfoTextElement(), canvas_element], PROJECT_TITLE, road_network_model_params
)

server.port = 8521
