import numpy as np
import pandas as pd
import random as rand
  
nombres_capitales = [
    "Ciudad de Buenos Aires",
    "Córdoba",
    "Corrientes",
    "Formosa",
    "La Plata",
    "La Rioja",
    "Mendoza",
    "Neuquen",
    "Paraná",
    "Posadas",
    "Rawson",
    "Resistencia",
    "Río Gallegos",
    "San Fernando del Valle de Catamarca",
    "San Miguel de Tucumán",
    "San Salvador de Jujuy",
    "Salta",
    "San Juan",
    "San Luis",
    "Santa Fe",
    "Santa Rosa",
    "Santiago del Estero",
    "Ushuaia",
    "Viedma"]
matriz_distancias=[]

def cargar_matriz_distancias():
    data = pd.read_excel('C:\\Users\\Usuario\\Desktop\\TablaCapitales.xlsx') 
    for i in range(24):
        matriz_distancias.append([])
        for j in range(24):
            matriz_distancias[i].append(data.iloc[i, j+1])  #me paro en cada fila (i) , columna(j) - el iloc es para ubicar una celda                                           
            if (np.isnan(matriz_distancias[i][j]) == True): #busco el vacio de la diagonal principal y le pongo valor cero
                matriz_distancias[j][j] = 0

def crearPoblacionInicial():    
    global cromosomas 
    cromosomas = []

    for i in range(cantPoblacionInicial):
        cromosomas.append(rand.sample(list(listaNumeros), 24))
        cromosomas[i].append(cromosomas[i][0])   

def calcularFuncionObjetivo():
    
    for i in range(cantPoblacionInicial):
        cromosoma = cromosomas[i]
        suma = 0
        for j in range (len(cromosoma)-1):
            distancia = matriz_distancias[cromosoma[j]][cromosoma[j+1]]
            suma += distancia
        funcion_obj[i] = suma

def calcularFitness():
    sumatoria = sum(funcion_obj)
    for i in range(cantPoblacionInicial):                          
        list_fitness[i] = (1 - (funcion_obj[i]/sumatoria))

def crearRuleta():
    ruleta = []
    sumas = [list_fitness[0]]
    for i in range(len(list_fitness)-1):
        sumas.append(sumas[i]+list_fitness[i+1]) #Armo la lista de fitness acumulada
    for i in range(50):
        rul = rand.uniform(0,1)
        for i in range(50):
            if (rul<=sumas[i]):
                ruleta.append(i)
                break
    return ruleta 

def crossoverCiclico(padre1, padre2):
    posActual=0 #variable aux 

    hijo1=[] #instancio los hijos
    hijo2=[]
    for _ in range(0, len(padre1)-1):   #les pongo a todos menos uno para indicar que no estan asignados     
        hijo1.append(-1)
        hijo2.append(-1)

    aux=padre1[0] #primer paso del ciclico
    
    while aux not in hijo1: #condicion de fin de ciclo
        hijo1[posActual] = aux
        aux = padre2[posActual]
        posActual = padre1.index(aux) 

    for j in range(0, len(padre1)-1):
        if (hijo1[j] == -1):
            hijo1[j] = padre2[j]
            hijo2[j] = padre1[j]
        else:
            hijo2[j] = padre2[j]  
    
    hijo1.append(hijo1[0])
    hijo2.append(hijo2[0])
    
    return hijo1,hijo2

def hacerMutacion(padre):
    aux = np.random.randint(2, size=30)      
    for x in range (len(padre)):
        aux[x]=padre[x]
    posicion = np.random.randint(0,len(aux)-1)
    if padre[posicion]==1:
        aux[posicion]=0
    else:
        aux[posicion]=1
    return aux

def crossover():
    ruleta=crearRuleta()
    hijos = []
    for _ in range (0,int(len(poblacion)/2)):
        padre_1 = rand.choice(ruleta)   
        padre_2 = rand.choice(ruleta)
        if (rand.random() <= prob_crossover):
            padre1,padre2=crossoverCiclico(padre1,padre2)
        
        #-------------MUTACION----------------------
        if (rand.random() <= prob_mutacion): 
            padre_1 = hacerMutacion(padre_1)  
        if (rand.random() <= prob_mutacion): 
            padre_2 = hacerMutacion(padre_2)

    return hijos


#MENU
listaNumeros = np.arange(0,24)
cantPoblacionInicial=50
prob_crossover=0.75
prob_mutacion=0.05
ciclos=200
promedios=[]
maximos=[]
minimos=[]
poblacion=[]
lista_optimo=[]
cromosomaOptimoFobj = 0
cromosomaOptimo = []
fobjOptima = 0
funcion_obj = list(np.zeros(cantPoblacionInicial)) #lo uso para inicializar los arreglos
list_fitness = list(np.zeros(cantPoblacionInicial))

def guardar():
    
    global cromosomaOptimo
    global cromosomaOptimoFobj
    global fobjOptima

    minimoObj = min(funcion_obj)
    minimos.append(minimoObj)
    maximos.append(max(funcion_obj))
    promedios.append(np.mean(funcion_obj))
    indice = funcion_obj.index(minimoObj)
    optimo = cromosomas[indice]
    
    lista_optimo.append(optimo)

    if (minimoObj < cromosomaOptimoFobj) or (cromosomaOptimoFobj == 0):
        cromosomaOptimoFobj = minimoObj
        cromosomaOptimo = optimo

def tabla():
    lista_excel = []
    lista_excel.append(list(range(1,ciclos+1)))
    lista_excel.append(promedios)
    lista_excel.append(maximos)
    lista_excel.append(minimos)
    df=pd.DataFrame(lista_excel)
    df = df.T
    df.columns = ['Corrida','Promedio FO','Maximo FO','Minimo FO']
    #with pd.ExcelWriter(ruta) as writer:
        #df.to_excel(writer, sheet_name='TP 1', index=False)   
    print(df)

cargar_matriz_distancias()
crearPoblacionInicial()
calcularFuncionObjetivo()
calcularFitness()
for x in range (ciclos):
    guardar()
    poblacion=crossover()
    funcion_obj = list(np.zeros(cantPoblacionInicial)) #inicializo de nuevo para que no me queden datos de la poblacion anterior
    list_fitness = list(np.zeros(cantPoblacionInicial))
    calcularFuncionObjetivo()
    calcularFitness()
tabla()
print("Cromosoma óptimo: ", cromosomaOptimo)
print("Función objetivo óptima: ", cromosomaOptimoFobj)
#print(promedios)