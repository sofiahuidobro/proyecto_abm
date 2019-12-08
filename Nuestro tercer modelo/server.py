##SEGUNDO ARCHIVO
from model import HumanCapital
from mesa.visualization.modules.CanvasGridVisualization import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

def definirColor(educarse,empleo_calificado):
    if educarse==False:
        return "yellow"
    else:
        if empleo_calificado==False:
            return "red"
        else:
            return "green"


#portrayal. dictionary de Python para la definición del diseño de los agentes:
def portrayal(agent):    
    portrayal = {"Shape": "rect",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": definirColor(agent.educarse,agent.empleo_calificado),
                 "text": agent.unique_id,
                 "text_color": "white",
                 "h":1.00,
                 "w":1.00}
    return portrayal


grid = CanvasGrid(portrayal,7,7,500,500)
chart = ChartModule([{"Label":"Nagentes","Color":"green"}],data_collector_name="datacollector")

server = ModularServer(HumanCapital,
                       [grid,chart],
                       "Nuestro segundo modelo",
                       {"N_buenos_empleo":UserSettableParameter('slider',"Numero de buenos empleos",5,1,50,1)})  