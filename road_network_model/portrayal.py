from road_network_model.agent import Car, Road, Office, Residence, Entertaint

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
        portrayal["scale"] = 10
        portrayal["Layer"] = 10
        portrayal["w"] = 0.5
        portrayal["h"] = 0.5
        portrayal["x"] = agent.current_coor[0]
        portrayal["y"] = agent.current_coor[1]
        portrayal["Filled"] = "true"
    if type(agent) is Road:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "grey"
        portrayal["scale"] = 10
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["x"] = agent.pos[0]
        portrayal["y"] = agent.pos[1]
        portrayal["Filled"] = "true"
    if type(agent) is Office:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "blue"
        portrayal["scale"] = 10
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["x"] = agent.pos[0]
        portrayal["y"] = agent.pos[1]
        portrayal["Filled"] = "true"
    if type(agent) is Residence:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "yellow"
        portrayal["scale"] = 10
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["x"] = agent.pos[0]
        portrayal["y"] = agent.pos[1]
        portrayal["Filled"] = "true"
    if type(agent) is Entertaint:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "green"
        portrayal["scale"] = 10
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["x"] = agent.pos[0]
        portrayal["y"] = agent.pos[1]
        portrayal["Filled"] = "true"

    return portrayal