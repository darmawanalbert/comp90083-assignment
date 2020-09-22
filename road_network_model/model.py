"""
Wolf-Sheep Predation Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from road_network_model.agents import Car


class Car(Model):
 
    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def step(self):
        """ step """

    def run_model(self, step_count=200):
        """ run model """

