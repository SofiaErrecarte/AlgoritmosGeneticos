import numpy as np
import random as rand
import matplotlib.pyplot as plt
import math
import pandas as pd
import os 
from os import system

######## ######## ######## ########

nombresCapital = [
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

lista_min = []
lista_max = []
lista_prom = []
lista_optimo = []

cromosomaOptimoFobj=0
cromosomaOptimo=[]
cant_poblacion = 50                       
ciclos = 200                        
prob_mutacion =  5               
prob_crossover = 75 
numeros = np.arange(0,24)
poblacion = []   
matriz_distancias = []

######## CARGA MATRIZ DE DISTANCIAS ########
def cargar_matriz_distancias():
    data = pd.read_excel('C:\\Users\\Usuario\\Desktop\\TablaCapitales.xlsx') 
    for i in range(24):
        matriz_distancias.append([])
        for j in range(24):
                matriz_distancias[i].append(data.iloc[i, j+1])                                             
                if (np.isnan(matriz_distancias[i][j]) == True):
                    matriz_distancias[j][j] = 0
######## GENERA CROMOSOMAS ########
def generaCromosomas():    
    poblacion = []
    for i in range(cant_poblacion):
        poblacion.append(rand.sample(list(numeros), 24))
        poblacion[i].append(poblacion[i][0])        
    return poblacion

######## FUNCION OBJETIVO ########         
def calcula_funcion_obj(poblacion):
    for i in range(cant_poblacion):
        poblacion = poblacion[i]
        suma = 0
        for j in range (len(poblacion)-1):
            distancia = matriz_distancias[poblacion[j]][poblacion[j+1]]
            suma += distancia
        funcion_obj[i] = suma
    return funcion_obj
######## list_fitness ########           
def calcula_list_fitness(funcion_obj):
    sumatoria = sum(funcion_obj)
    for i in range(cant_poblacion):                          
        list_fitness[i] = (1 - (funcion_obj[i]/sumatoria))
    return list_fitness

######## RULETA ########              
def calcula_ruleta():

    nuevolist_fitness = list(np.zeros(cant_poblacion))
    sumalist_fitness = sum(list_fitness)
    for i in range(len(list_fitness)):
        nuevolist_fitness[i] = (list_fitness[i]/sumalist_fitness)
    frec_acum = []
    frec_acum.append(nuevolist_fitness[0])
    for i in range(1,cant_poblacion):
        acumulado = frec_acum[i - 1] + nuevolist_fitness[i]
        frec_acum.append(acumulado)

    return frec_acum


######## TIRADA DE RULETA ########             
def tiradas(ruleta):
    padres = []
    for m in range(2):
        frec = rand.uniform(0,1)

        for i in range(cant_poblacion):
            if(ruleta[i] > frec):
                cromosomas[i].pop()
                padres.append(cromosomas[i]) 
                cromosomas[i].append(cromosomas[i][0])     
                break

    return padres[0], padres[1]
 

######## CROSSOVER CICLICO ########            
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
    #print('hijo1 ', hijo1)
    #print('hijo2', hijo2)
    return hijo1,hijo2

######## SELECCION Y CROSSOVER ########           
def selec_cross(list_fitness, poblacion):

    ruleta = calcula_ruleta(list_fitness)
    aux = np.array(funcion_obj)
    min1 = aux.argsort()[0]
    min2 = aux.argsort()[1]
    aux = list(aux)
    aux[0] = poblacion[min1]
    aux[1] = poblacion[min2]

    for i in range(2, len(poblacion)-1, 2):
        c1,c2 = tiradas(ruleta)
        c1,c2 = crossoverCiclico(c1,c2)
        aux[i] = c1
        aux[i+1] = c2
    poblacion = aux[:]
    return poblacion

######## MUTACION ########         
def mutacion():
    for i in range(len(cromosomas)):
        x = np.random.randint(0, 101)
        cromosomas[i].pop()             
        if x <= prob_mutacion:                                     
            posicion1 = np.random.randint(0, len(nombresCapital))
            posicion2 = np.random.randint(0, len(nombresCapital))
            aux1 = cromosomas[i][posicion1]
            aux2 = cromosomas[i][posicion2]
            cromosomas[i][posicion1] = aux2
            cromosomas[i][posicion2] = aux1
        cromosomas[i].append(cromosomas[i][0])



######## SALIDA DE ALGORITMO GENETICO ########
def muestraGrafica():

    generacion = np.arange(1, ciclos + 1)
    
    ######## TABLA EXCEL ########
    Datos = pd.DataFrame({"Generacion": generacion, "Minimo FO": lista_min, "Maximo FO": lista_max, "Promedio FO": lista_prom})  
    Tabla = pd.ExcelWriter('C:\\Users\\Usuario\\Desktop\\Tabla.xlsx', engine='xlsxwriter') 
    Datos.to_excel(Tabla, sheet_name='Valores', index = False)     

    workbook = Tabla.book
    worksheet = Tabla.sheets["Valores"] 

    formato = workbook.add_format({"align": "center"})

    worksheet.set_column("A:D", 15, formato)  
    worksheet.conditional_format("D1:DF"+str(len(lista_prom)+1), {"type": "3_color_scale", "max_color": "red", "mid_color": "yellow", "min_color": "green"})

    Tabla.save()

######## GUARDA LISTAS ########
def guardaListas(funcion_obj, poblacion):

    global cromosomaOptimo
    global cromosomaOptimoFobj
    global fobjOptima

    minimoObj = min(funcion_obj)
    lista_min.append(minimoObj)
    lista_max.append(max(funcion_obj))
    lista_prom.append(np.mean(funcion_obj))
    indice = funcion_obj.index(minimoObj)
    optimo = poblacion[indice]
    
    lista_optimo.append(optimo)

    if (minimoObj < cromosomaOptimoFobj) or (cromosomaOptimoFobj == 0):
        cromosomaOptimoFobj = minimoObj
        cromosomaOptimo = optimo
        
cargar_matriz_distancias()
cant_poblacion =50                         
ciclos = 200                     
prob_mutacion =  0.05                
prob_crossover = 0.75    

funcion_obj = list(np.zeros(cant_poblacion))
list_fitness = list(np.zeros(cant_poblacion))

poblacion=generaCromosomas()
funcion_obj = calcula_funcion_obj(poblacion)
list_fitness = calcula_list_fitness(funcion_obj)

for i in range(ciclos):
    guardaListas(funcion_obj,poblacion)
    selec_cross(list_fitness,poblacion=)
    mutacion()
    funcion_obj = list(np.zeros(cant_poblacion))
    list_fitness = list(np.zeros(cant_poblacion))
    calcula_funcion_obj()
    calcula_list_fitness()
muestraGrafica()

print()
print("Cromosoma óptimo: ", cromosomaOptimo)
print("Función objetivo óptima: ", cromosomaOptimoFobj)
lista_min = []
lista_max = []
lista_prom = []
lista_optimo = []
cromosomaOptimoFobj = 0
cromosomaOptimo = []
fobjOptima = 0

