#!/usr/bin/env python
# coding: utf-8


#Proyecto de retornos a la educación
#Autores: Alejandro Arellano Best, Joaquín Fosado, Ricardo Carpio y Sofía Huidobro


#Dado que estamos corriendo el modelo en Notebook, primero se tiene que definir el modelo con la definición de los agentes y luego el del entorno. 
#Les voy a dejar espacios para que lo escriban. (si ustedes prefieren trabajar en spyder u otro idle, hacemos docs separados y al final lo juntamos todo en el notebook)


# # Espacio para agentes



# # Espacio para entorno



popo


# Definición del grid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer 
from model import EducModel

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
        "Color": "red",
        "Filled": "true",
        "Layer": 0,
        "r": 0.5}
    return portrayal

grid = CanvasGrid(agent_portrayal, 7, 7, 500, 500)

server = ModularServer(EducModel,
    [grid],
    "Education Model",
    {"N":49, "width":7, "height":7})
server.port = 8521
server.launch()

# Incorporar agentes al grid
def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
        "Filled": "true",
        "r": 0.5}
    if agent.salary>2: #Aquí estoy pensando que lo que observamos (el outcome) es el salario del individuo. 
        #Sabemos que si el salario=1 obtuvo empleo no calificado y si salario>2 obtuvo empleo calificado (por ende se educó)
        #Habrá que pensar en una manera de ver a los que sí se educaron pero no obtuvieron el empleo.
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    return portrayal

from mesa.visualization.modules import ChartModule



