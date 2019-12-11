#Librerías
from model import HumanCapital
from mesa.visualization.modules.CanvasGridVisualization import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

#Asignación de colores en función de la educacióon y del tipo de empleo
def definirColor(educarse,empleo_calificado):
    if educarse==False:
        return "yellow" #No educado
    else:
        if empleo_calificado==False:
            return "red" #Educado sin trabajo calificado
        else:
            return "green" #Educado con trabajo calificado


#Portrayal
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

#Definición de lo elementos del server
grid = CanvasGrid(portrayal,7,7,500,500)
chart = ChartModule([{"Label":"Empleo calificado","Color":"green"},{"Label":"Educados sin empleo calificado","Color":"red"},{"Label":"No educados","Color":"yellow"}],data_collector_name="datacollector")

#Definición del server
server = ModularServer(HumanCapital,
                       [grid,chart],
                       "Modelo de Capital Humano",
                       {"N_educados":UserSettableParameter('slider',"Numero de personas educadas",20,1,50,1),
                       "N_buenos_empleo":UserSettableParameter('slider',"Numero de empleos calificados",10,1,50,1),
                       "colegiatura":UserSettableParameter('slider',"Colegiatura",10,0,25,1)})