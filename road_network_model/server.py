from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from road_network_model.agents import Car
from road_network_model.model import Car


def car_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Car:
        portrayal["Shape"] = "" # ex: road_network_model/resources/car.png
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    return portrayal

canvas_element = CanvasGrid(car_portrayal, 20, 20, 500, 500)

model_params = {
    "checkbox_param": UserSettableParameter("checkbox", "is Enabled", True),
    "slider_param": UserSettableParameter(
        "slider", "Slider Params", 20, 1, 50
    )
}

server = ModularServer(
    Car, [canvas_element], "Odd-Even Rationing Control", model_params
)

server.port = 8521
