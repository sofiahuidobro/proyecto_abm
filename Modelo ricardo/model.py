# -*- coding: utf-8 -*
"""
Created on Sat Nov 16 22:29:03 2019

@author: Ricardo
"""

###LIBRERÍAS.
from mesa import Agent,Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

###AGENTES.
class Agente(Agent):
    ##Inicialización del agente.
    def __init__(self,unique_id,model):
        super().__init__(unique_id,model)
        self.salario=self.random.randint(-1,1)
        if self.salario==-1:
            self.color="red"
        elif self.salario==0:
            self.color="yellow"
        else:
            self.color="green"
        self.salario_esperado=1 #¿debería ser 1?
        self.primera_generacion=True
        self.educarse = True
        self.pos = [0,0]
        if self.random.randint(0,49) < 20:
            self.educado = True
            if self.random.randint (0,49) < 10:
                self.empleo_calificado = True
            else:
                self.empleo_calificado = False
        else:
            self.educado = False
            self.empleo_calificado = False
    ##Reglas de comportamiento.
    def step(self):
        #Agente viejo.
        if self.primera_generacion==False:
            print("viejo")
            #Caso no educado.
            if self.educarse==False:
                self.salario+=1
                self.color="yellow"
            #Caso educado.
            else:
                #Proceso que asigna trabajos calificados y no calificados:
                ParamProb=self.random.randint(0,9)
                #Caso agente con estudios y trabajo no calificado.
                if ParamProb<=6:
                    self.empleo_calificado=False
                    self.salario+=1
                    self.color="red"
                #Caso agente con estudios y trabajo calificado.
                else:
                    self.empleo_calificado=True
                    self.salario+=2.5
                    self.color="green"
        #Agente joven.
        else:
            print("joven")
            #Cálculo del salario esperado.
            vecinos=self.model.grid.get_neighbors(self.pos,moore=True,include_center=False)
            suma=0
            for v in vecinos:
                suma+=v.salario
                self.salario_esperado=suma/len(vecinos)
            #Caso educarse: paga por la educación.
            if self.salario<=self.salario_esperado:
                self.educarse=True
                self.salario-=0.25 
            #Caso no educarse: recibe trabajo no calificado.
            else:
                self.educarse=False
                self.salario+=1
                self.color="yellow"
            #Se falsea la primera generación.
            self.primera_generacion=False

##Métodos del modelo.
def contarAgentes2(model):
    return model.schedule.get_agent_count()    

def contarAgentes(model): #CAMBIAR EL NOMBRE Y HACERLO PARA LOS OTROS TIPOS
    n = 0
    for i in model.schedule.agents:
        if i.empleo_calificado==True:
            n +=1
    return n

def getCurrentTick(model):
    return model.schedule.steps  
     
###MODELO.
class HumanCapital(Model):
    ##Inicialización del modelo.
    def __init__(self,N_buenos_empleo,seed=None):
        self.current_id=0
        self.running = True
        self.width=7
        self.height=7
        # Definimos el schedule para hacer la ejecucion en orden aleatorio
        self.schedule = RandomActivation(self)
        #Definimos el grid de tamanio 7x7 y sin fronteras flexibles
        self.grid = MultiGrid(self.width,self.height,False)
        ##Declaración del grid.
        for y in range(0,self.height):
            for x in range(0,self.width):
                a=Agente(self.next_id(),self)
                self.schedule.add(a)
                self.grid.place_agent(a, [x,y])
        self.datacollector = DataCollector(
            model_reporters={"Nagentes": contarAgentes,"NumberTicks":getCurrentTick})
        
    ##Itinerario.    
    def step(self):
        #Ejecutar el step de los agentes.
        self.schedule.step()
        #Ejecutar el datacollector
        self.datacollector.collect(self)
        
        # Esta sección indica a model cuando detenerse. En el caso del modelo de
        # capital humano, no habría un parámetro de temrinación definido. Discutir.
        #if self.schedule.get_agent_count()<2:
        #    self.running = False