##SEGUNDO ARCHIVO
from model import miModelo
from mesa.visualization.modules.CanvasGridVisualization import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

#portrayal. dictionary de Python para la definición del diseño de los agentes:
def portrayal(agent):    
    portrayal = {"Shape": "rect",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": agent.color,
                 "text": agent.unique_id,
                 "text_color": "white",
                 "h":1.00
                 "w":1.00}
    return portrayal

grid = CanvasGrid(portrayal,10,10,500,500)
chart = ChartModule([{"Label":"Nagentes","Color":"red"}],data_collector_name="datacollector")

server = ModularServer(miModelo,
                       [grid,chart],
                       "Nuestro segundo modelo",
                       {"N":UserSettableParameter('slider',"Numero de agentes",5,1,50,1)})  