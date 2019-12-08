#Librerías
from mesa import Agent,Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

#Agente
class Agente(Agent):
    #Inicialización del agente
    def __init__(self,unique_id,model, N_buenos_empleo, N_educados,colegiatura):
        super().__init__(unique_id,model)
        self.salario= self.random.random()
        self.pos = [0,0]
        self.N_buenos_empleo = N_buenos_empleo
        self.N_educados = N_educados
        self.colegiatura = colegiatura
        #Aleatorización inicial de educación y trabajo calificado
        if self.random.randint(0,49) < self.N_educados:
            self.educarse = True
            if self.random.randint (0,49) < self.N_buenos_empleo:
                self.empleo_calificado = True
                self.señal = 1
            else:
                self.empleo_calificado = False
                self.señal = -1
        else:
            self.educarse = False
            self.empleo_calificado = False
            self.señal = 0

    ##Reglas de comportamiento.
    def step(self):
        #Cálculo de retorno a la educación
        vecinos=self.model.grid.get_neighbors(self.pos,moore=True,include_center=True)
        indice=0
        for v in vecinos:
            indice += v.señal
        #Decisión de estudiar con base en la indice
        if indice >= 0 and self.salario >= self.colegiatura:
            self.educarse=True
            self.salario -= self.colegiatura
            if self.random.randint (0,49) < self.N_buenos_empleo:
                self.empleo_calificado = True
                self.salario += 2.5
                self.color = "green"
                self.señal = 1
            else:
                self.empleo_calificado = False
                self.salario += 1
                self.color = "red"
                self.señal = -1
        else:
            self.educarse = False
            self.empleo_calificado = False
            self.salario += 1
            self.color="yellow"
            self.señal = 0

#Modelo
class HumanCapital(Model):
    ##Inicialización del modelo.
    def __init__(self, N_buenos_empleo=10, N_educados=20,colegiatura=0.25,seed=None):
        self.current_id=0
        self.running = True
        self.width=7
        self.height=7
        self.N_buenos_empleo = N_buenos_empleo
        self.N_educados = N_educados
        self.colegiatura = colegiatura
        # Definimos el schedule para hacer la ejecucion en orden aleatorio
        self.schedule = RandomActivation(self)
        #Definimos el grid de tamanio 7x7 y sin fronteras flexibles
        self.grid = MultiGrid(self.width,self.height,False)
        ##Declaración del grid.
        for y in range(0,self.height):
            for x in range(0,self.width):
                a=Agente(self.next_id(),self,  N_buenos_empleo, N_educados,colegiatura)
                self.schedule.add(a)
                self.grid.place_agent(a, [x,y])
        self.datacollector = DataCollector(
            model_reporters={"Empleo calificado": contarAgentesCal,"NumberTicks":getCurrentTick, "Educados": contarAgentesEdu, "No educados":contarAgentesNoEdu})

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

#Métodos del modelo
def contarAgentes(model):
    return model.schedule.get_agent_count()

def contarAgentesCal(model): #Contar agentes con empleo calificado
    n = 0
    for i in model.schedule.agents:
        if i.empleo_calificado==True:
            n +=1
    return n

def contarAgentesEdu(model): #Contar agentes educados
    n = 0
    for i in model.schedule.agents:
        if i.educarse==True:
            n +=1
    return n

def contarAgentesNoEdu(model): #Contar agentes no educados
    n = 0
    for i in model.schedule.agents:
        if i.educarse==False:
            n +=1
    return n

def getCurrentTick(model):
    return model.schedule.steps