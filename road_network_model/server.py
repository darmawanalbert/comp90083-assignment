from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from road_network_model.agent import Car, TrafficLight
from road_network_model.model import RoadNetworkModel
from road_network_model.portrayal import road_network_model_portrayal
from road_network_model.constant import PROJECT_TITLE, CANVAS_WIDTH, CANVAS_HEIGHT, GRID_WIDTH, GRID_HEIGHT, NUMBER_OF_CARS

import math

# Define a CanvasGrid to visualise the Road Network Model
canvas_element = CanvasGrid(road_network_model_portrayal, GRID_WIDTH, GRID_HEIGHT, CANVAS_WIDTH, CANVAS_HEIGHT)

chart_car_state = ChartModule(
    [
        {"Label": "Idle", "Color": "#FF0000"},
        {"Label": "Move", "Color": "#00FF00"},
        {"Label": "Finished", "Color": "#0000FF"}
    ]
)

chart_car_moving = ChartModule(
    [
        {"Label": "ToOffice", "Color": "#F1C40F"},
        {"Label": "ToResidence", "Color": "#2C3E50"}
    ]
)

class InfoTextElement(TextElement):
    def render(self, model):
        # Mean Travel Time
        mean_travel_time = model.mean_travel_time
        mean_travel_time_text = "{0:.2f}".format(mean_travel_time)

        # Time
        current_time = model.tick % 1440
        hour = math.floor(current_time / 60)
        minute = current_time % 60
        hour_text = "0" + str(hour) if hour < 10 else str(hour)
        minute_text = "0" + str(minute) if minute < 10 else str(minute)
        time_text = hour_text + ":" + minute_text

        return "<b>Info</b><br>Mean Travel Time: {} minutes<br>Time: {}".format(mean_travel_time_text, time_text)

class LegendsTextElement(TextElement):
    def render(self, model):
        legends_text = "<br><b>Legends</b><br><br>"
        legends_text += "<table>"
        
        legends_text += "<tr>"
        legends_text += "<td>"
        legends_text += "Road"
        legends_text += "</td>"
        legends_text += "<td>"
        legends_text += "&nbsp; &nbsp;"
        legends_text += "</td>"
        legends_text += "<td style='text-align: center; vertical-align: middle;'>"
        legends_text += "<p style='border: 3px solid grey; width: 20px; height: 3px; '>&nbsp;</p>"
        legends_text += "</td>"
        legends_text += "</tr>"

        legends_text += "<tr>"
        legends_text += "<td>"
        legends_text += "Intersection"
        legends_text += "</td>"
        legends_text += "<td>"
        legends_text += "&nbsp; &nbsp;"
        legends_text += "</td>"
        legends_text += "<td style='text-align: center; vertical-align: middle;'>"
        legends_text += "<p style='border: 3px solid #333333; width: 20px; height: 3px; '>&nbsp;</p>"
        legends_text += "</td>"
        legends_text += "</tr>"

        legends_text += "<tr>"
        legends_text += "<td>"
        legends_text += "Residence"
        legends_text += "</td>"
        legends_text += "<td>"
        legends_text += "&nbsp; &nbsp;"
        legends_text += "</td>"
        legends_text += "<td style='text-align: center; vertical-align: middle;'>"
        legends_text += "<p style='border: 3px solid yellow; width: 20px; height: 3px; '>&nbsp;</p>"
        legends_text += "</td>"
        legends_text += "</tr>"

        legends_text += "<tr>"
        legends_text += "<td>"
        legends_text += "Entertainment"
        legends_text += "</td>"
        legends_text += "<td>"
        legends_text += "&nbsp; &nbsp;"
        legends_text += "</td>"
        legends_text += "<td style='text-align: center; vertical-align: middle;'>"
        legends_text += "<p style='border: 3px solid green; width: 20px; height: 3px; '>&nbsp;</p>"
        legends_text += "</td>"
        legends_text += "</tr>"

        legends_text += "<tr>"
        legends_text += "<td>"
        legends_text += "Office"
        legends_text += "</td>"
        legends_text += "<td>"
        legends_text += "&nbsp; &nbsp;"
        legends_text += "</td>"
        legends_text += "<td style='text-align: center; vertical-align: middle;'>"
        legends_text += "<p style='border: 3px solid blue; width: 20px; height: 3px; '>&nbsp;</p>"
        legends_text += "</td>"
        legends_text += "</tr>"

        legends_text += "<tr>"
        legends_text += "<td>"
        legends_text += "Car (Odd plate)"
        legends_text += "</td>"
        legends_text += "<td>"
        legends_text += "&nbsp; &nbsp;"
        legends_text += "</td>"
        legends_text += "<td style='text-align: center; vertical-align: middle;'>"
        legends_text += "<p style='border: 3px solid #FF00FF; width: 20px; height: 3px; '>&nbsp;</p>"
        legends_text += "</td>"
        legends_text += "</tr>"

        legends_text += "<tr>"
        legends_text += "<td>"
        legends_text += "Car (Even plate)"
        legends_text += "</td>"
        legends_text += "<td>"
        legends_text += "&nbsp; &nbsp;"
        legends_text += "</td>"
        legends_text += "<td style='text-align: center; vertical-align: middle;'>"
        legends_text += "<p style='border: 3px solid red; width: 20px; height: 3px; '>&nbsp;</p>"
        legends_text += "</td>"
        legends_text += "</tr>"

        legends_text += "</table>"
        legends_text += "<br><br><b>Car State</b>"
        return legends_text

class LegendsTextElement2(TextElement):
    def render(self, model):
        legends_text = "<br><br><b>Car Moving</b>"
        return legends_text

policy_range_time = [
    '7_10_and_16_19',
    '8_11_and_17_20',
    '6_9_and_15_18',
    '8_9_and_17_18',
    '6_11_and_15_20'
]

# Define parameter of Road Network Model
road_network_model_params = {
    "number_of_cars": NUMBER_OF_CARS,
    "width": GRID_WIDTH,
    "height": GRID_HEIGHT,
    "is_odd_even_policy_enabled": UserSettableParameter("checkbox", "Odd-Even Policy Enabled", True),
    "is_odd_date": UserSettableParameter("checkbox", "Is Odd Date", True),
    "policy_range_time": UserSettableParameter('choice', 'Range Time (in hours)', value='7_10_and_16_19', choices=policy_range_time)
}

# Instantiate the server at port 8521
server = ModularServer(
    RoadNetworkModel, [InfoTextElement(), canvas_element, LegendsTextElement(), chart_car_state, LegendsTextElement2(), chart_car_moving], PROJECT_TITLE, road_network_model_params
)

server.port = 8521
