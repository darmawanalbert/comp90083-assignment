from road_network_model.agent import Car, Road

def road_network_model_portrayal(agent):
    """
    This function is registered with the visualization server to be called
    each tick to indicate how to draw the car in its current state.
    :param agent:  the car in the simulation
    :return: the portrayal dictionary.
    """
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Car:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "red"
        portrayal["scale"] = 1
        portrayal["Layer"] = 1
        portrayal["w"] = 0.5
        portrayal["h"] = 0.5
        portrayal["x"] = agent.source[0]
        portrayal["y"] = agent.source[1]
        portrayal["Filled"] = "true"
    if type(agent) is Road:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "grey"
        portrayal["scale"] = 1
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["x"] = agent.pos[0]
        portrayal["y"] = agent.pos[1]
        portrayal["Filled"] = "true"

    return portrayal