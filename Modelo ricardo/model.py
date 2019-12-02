# -*- coding: utf-8 -*-
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
        self.salario_esperado=0
        self.educado=False
        self.primera_generacion=True
        self.sumUneducated=0
        self.sumEducatedSkilled=0
    ##Reglas de comportamiento.
    def step(self):
        #Agente viejo.
        if self.primera_generacion==False:
            #Caso no educado.
            if self.educarse==False:
                self.salario+=1
            #Caso educado.
            else:
                #Proceso que asigna trabajos calificados y no calificados:
                ParamProb=self.random.randint(0,9)
                if ParamProb<=6:
                    self.empleo_calificado=False
                else:
                    self.empleo_calificado=True
                #Caso agente con estudios y trabajo no calificado.
                if self.empleo_calificado==False:
                    self.salario+=1
                    #Esta sección cambia el tipo que tenga el agente en el grid a uno EducatedUnskilled.
                    self.model.grid.remove_agent(self)
                    c=EducatedUnskilled(unique_id,model)
                    self.model.grid.place_agent(c,self)
                #Caso agente con estudios y trabajo calificado.
                else:
                    self.salario+=2.5
                    #Esta sección cambia el tipo que tenga el agente en el grid a uno EducatedSkilled.
                    self.model.grid.remove_agent(self)
                    c=EducatedSkilled(unique_id,model)
                    self.model.grid.place_agent(c,self)
        #Agente joven.
        else:
        #Obtención de información acerca del tipo de agente del entorno usando len(vecinos)>0.
        vecinos=self.model.grid.get_neighbors(self.pos,moore=True,include_center=True,radius=0)
        UneducatedNeighbors=[x for x in vecinos if type(x) is Uneducated and x!=self]
        EducatedSkilledNeighbors=[x for x in vecinos if type(x) is EducatedSkilled and x!=self]
        if len(UneducatedNeighbors)>0:
            self.sumUneducated=-1*len(UneducatedNeighbors)
        else:
            self.sumUneducated=0
        if len(EducatedSkilledNeighbors)>0:
            self.sumEducatedSkilled=1*len(EducatedSkilledNeighbors)
        else:
            self.sumEducatedSkilled=0
        #Cálculo del salario esperado.
        self.salario_esperado=self.sumUneducated+self.sumEducatedSkilled
        #Selección de estrategia: estudiar o trabajar.
        if self.salario<=self.salario_esperado:
            self.educarse=True
        else:
            self.educarse=False
        #Caso no educarse: recibe trabajo no calificado.
        if self.educarse==False:
            self.salario+=1
            #Esta sección cambia el tipo que tenga el agente en el grid a uno Uneducated.
            self.model.grid.remove_agent(self)
            c=Uneducated(unique_id,model)
            self.model.grid.place_agent(c,self)
        #Caso educarse: paga por la educación.
        else:
            self.salario-=0.25
        #Se falsea la primera generación.
        self.primera_generacion=False     

class Uneducated(Agent):
    def __init__(self,unique_id,model):
        super().__init__(unique_id,model)
        color = "red"
        self.color = color

class EducatedUnskilled(Agent):
    def __init__(self,unique_id,model):
        super().__init__(unique_id,model)
        color = "yellow"
        self.color = color

class EducatedSkilled(Agent):
    def __init__(self,unique_id,model):
        super().__init__(unique_id,model)
        color = "green"
        self.color = color
    
##Métodos del modelo.
#AVISO: ¡REPROGRAMAR!
#def contarAgentes(model):
#    return model.schedule.steps  
#def getCurrentTick(model):
#    return model.schedule.get_agent_count()      
     
###MODELO
class HumanCapital(Model):
    ##Inicialización del modelo.
    def __init__(self,N,seed=None):
        self.current_id=0
        self.running = True
        # Definimos el schedule para hacer la ejecucion en orden aleatorio
        self.schedule = RandomActivation(self)
        #Definimos el grid de tamanio 7x7 y sin fronteras flexibles
        self.grid = MultiGrid(7,7,False)
        ##Declaración del grid.
        for y in range(0,height):
            for x in range(0,width):
                a=Agente(self.next_id(),self)
                self.schedule.add(a)
                self.grid.place_agent(a, [x,y])
                #Asignación de tipo de Agente en el grid.
                if self.schedule.salario(i)==-1:
                    b=Uneducated(self.next_id(),self)
                elif self.schedule.salario(i)==0:
                    b=EducatedUnskilled(self.next_id(),self)
                elif self.schedule.salario(i)==1:
                    b=EducatedSkilled(self.next_id(),self)
                self.grid.place_agent(b,[x,y])

        ##AVISO: ¡REPROGRAMAR!
        #self.datacollector = DataCollector(
        #    model_reporters={"Nagentes": contarAgentes,"NumberTicks":getCurrentTick})
        
    ##Itinerario.    
    def step(self):
        #Ejecutar el step de los agentes.
        self.schedule.step()
        #AVISO: ¡REPROGRAMAR!
        #self.datacollector.collect(self)
        
        # Esta sección indica a model cuando detenerse. En el caso del modelo de
        # capital humano, no habría un parámetro de temrinación definido. Discutir.
        #if self.schedule.get_agent_count()<2:
        #    self.running = False
