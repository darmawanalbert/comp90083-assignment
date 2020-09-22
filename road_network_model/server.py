from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from wolf_sheep.agents import Wolf, Sheep, GrassPatch
from wolf_sheep.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Car:
        portrayal["Shape"] = "" # ex: road_network_model/resources/car.png
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    return portrayal


server = ModularServer(
    Car, [canvas_element, chart_element], "Odd-Even Rationing Control", model_params
)

server.port = 8521
