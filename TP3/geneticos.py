from typing import runtime_checkable
import numpy as np
import random as rand
from numpy.core.numeric import zeros_like
import pandas as pd

cant_poblacion = 50
listaNumeros = np.arange(0,24)
matriz_distancias = []
prob_mutacion= 0.05
prob_crossover=0.9
ciclos=200
minimos=[]
maximos=[]
promedios=[]
optimos=[]
valor_cromosoma_optimo=0
cromosoma_optimo=[]
ruta = "C:\\Users\\Usuario\\Desktop\\Tabla.xlsx"

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

def cargaMatrizDeDistancias():
    data = pd.read_excel('C:\\Users\\Usuario\\Desktop\\TablaCapitales.xlsx') 
    for i in range(24):
        matriz_distancias.append([])
        for j in range(24):
                matriz_distancias[i].append(data.iloc[i, j+1])                                             
                if (np.isnan(matriz_distancias[i][j]) == True):
                    matriz_distancias[j][j] = 0

def crear_poblacion():    
    poblacion = []
    for i in range(cant_poblacion):
        poblacion.append(rand.sample(list(listaNumeros), 24))
        poblacion[i].append(poblacion[i][0])        
    return poblacion

def calcular_funcion_objetivo(poblacion):
    funcion_obj = []
    for i in range(len(poblacion)):
        suma = 0
        for j in range(len(poblacion[i])-1):
            suma += matriz_distancias[poblacion[i][j]][poblacion[i][j+1]]
        suma+=matriz_distancias[poblacion[i][j+1]][poblacion[i][0]]
        funcion_obj.append(suma)
    print(min(funcion_obj))
   
    return funcion_obj

def calcular_fitness(funcion_obj):
    list_fitness= list(np.zeros(cant_poblacion))
    for i in range(cant_poblacion):                          
        list_fitness[i] = (1/funcion_obj[i])
    sumatoria = 0
    for i in range(len(list_fitness)):
        sumatoria += list_fitness[i]
    for i in range(len(list_fitness)):
        list_fitness[i] = list_fitness[i]/sumatoria
    print(sum(list_fitness))
    return list_fitness

def crear_ruleta(list_fitness):
    ruleta = []
    acumulado = [list_fitness[0]]
    for i in range(len(list_fitness)-1):
        acumulado.append(acumulado[i]+list_fitness[i+1]) #Armo la lista de fitness acumulada
    for i in range(cant_poblacion):
        rul = rand.uniform(0,1)
        for i in range(cant_poblacion):
            if (rul<=acumulado[i]):
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
    #print('hijo1 ', hijo1)
    #print('hijo2', hijo2)
    return hijo1,hijo2

def elitismo(nuevaPoblacion,list_fitness):
    ind_ordenes = []
    #aux = lista_fit.copy()

    ind_ordenes = np.argsort(list_fitness) #Ordena los indices de menor a mayor
    list(ind_ordenes)
    #print(len(ind_ordenes))
    #print(ind_ordenes)
    for i in range(10):
        #print(len(ind_ordenes)-(i+1))
        nuevaPoblacion.append(poblacion[ind_ordenes[len(ind_ordenes)-(i+1)]])  #Agrega el miembro con el indice del mejor fitness, de mayor a menor.
       
        
    #print(len(nuevaPoblacion))
    return nuevaPoblacion

def crossover(poblacion,list_fitness,funcion_obj):
    ruleta = crear_ruleta(list_fitness)
    x = rand.uniform(0,1)
    nuevaPoblacion = []
    i = 0
    for j in range(25): #20 chances de crossover entre 40 miembros.
        if(x<=prob_crossover):
            nuevoCromo = []
            for k in range(24):
                nuevoCromo.append(31) #31 es un valor default para saber que fue cambiado y que no.
            ind1 = ruleta[i]
            ind2 = ruleta[i+1]        
            reco1 = poblacion[ind1]
            reco2 = poblacion[ind2]    # Selecciono dos recorridos con la ruleta.
            for k in range(len(reco1)):
                if (k==0):
                    nuevoCromo[0] = reco1[0]
                    vola = reco2[0]
                else:
                   dumpind =  reco1.index(vola)    
                   nuevoCromo[dumpind] = reco1[dumpind]
                   vola = reco2[dumpind]
                   if(reco2[dumpind] == reco1[0]):               
                       break            
            for k in range(len(nuevoCromo)):
                if(nuevoCromo[k]==31):
                    nuevoCromo[k] = reco2[k]
            nuevaPoblacion.append(nuevoCromo) #Agrego nuevo recorrido a la poblacion
            
            #Realizo mismo proceso forma simétrica.

            nuevoCromo = []
            for k in range(24):
                nuevoCromo.append(31)
            ind1 = ruleta[i+1]
            ind2 = ruleta[i]   
            reco1 = poblacion[ind1]
            reco2 = poblacion[ind2]   
            for k in range(len(reco1)):
                if (k==0):
                    nuevoCromo[0] = reco1[0]
                    vola = reco2[0]
                else:
                    dumpind =  reco1.index(vola) 
                    nuevoCromo[dumpind] = reco1[dumpind]
                    vola = reco2[dumpind]
                    if(reco2[dumpind] == reco1[0]):             
                        break 
                  
            for k in range(len(nuevoCromo)):
                if(nuevoCromo[k]==31):
                    nuevoCromo[k] = reco2[k]
            nuevaPoblacion.append(nuevoCromo)
            i+=2 #Aumento en 2 el bucle for



        elif(x>prob_crossover):
            nuevaPoblacion.append(poblacion[i])
            nuevaPoblacion.append(poblacion[i+1])
            i+=2
    #print(len(nuevaPoblacion))
    return nuevaPoblacion

def mutacion(nuevaPoblacion):
    """ Chequea mutación para los 40 miembros post-crossover"""
    for i in range(40):
        x = rand.uniform(0,1)
        #print(nuevaPoblacion[i])
        if(x<=prob_mutacion):
            #print("muto jojo")
            ale1 = rand.randrange(0,23)
            ale2 = rand.randrange(0,23)
            #print(ale1)
            #print(ale2)
            while(ale2 == ale1):
                ale2 = rand.randrange(0,23)
            aux = nuevaPoblacion[i][ale1]
            nuevaPoblacion[i][ale1] = nuevaPoblacion[i][ale2]
            nuevaPoblacion[i][ale2] = aux
            #print(nuevaPoblacion[i])
    return nuevaPoblacion
def tabla():
    generacion = np.arange(1, ciclos + 1)
    
    ######## TABLA EXCEL ########
    Datos = pd.DataFrame({"Generacion": generacion, "Minimo FO": minimos, "Maximo FO": maximos, "Promedio FO": promedios,"Optimo":optimos})  
    Tabla = pd.ExcelWriter('C:\\Users\\Usuario\\Desktop\\Tabla.xlsx', engine='xlsxwriter') 
    Datos.to_excel(Tabla, sheet_name='Valores', index = False)     

    workbook = Tabla.book
    worksheet = Tabla.sheets["Valores"] 

    formato = workbook.add_format({"align": "center"})

    worksheet.set_column("A:D", 15, formato)  
    worksheet.conditional_format("D1:DF"+str(len(promedios)+1), {"type": "3_color_scale", "max_color": "red", "mid_color": "yellow", "min_color": "green"})

    Tabla.save()
cargaMatrizDeDistancias()
poblacion= crear_poblacion()
print('Poblacion inicial: ',poblacion)
for i in range(ciclos):
    funcion_obj = calcular_funcion_objetivo(poblacion)
    list_fitness = calcular_fitness(funcion_obj)
    minimoObj = min(funcion_obj)
    minimos.append(minimoObj)
    maximos.append(max(funcion_obj))
    promedios.append(np.mean(funcion_obj))
    indice = funcion_obj.index(minimoObj)
    optimo = poblacion[indice]
    optimos.append(optimo)
    if (minimoObj < valor_cromosoma_optimo) or (valor_cromosoma_optimo == 0):
        valor_cromosoma_optimo = minimoObj
        cromosoma_optimo = optimo
    nuevaPoblacion=crossover(poblacion,list_fitness,funcion_obj)
    nuevaPoblacion=mutacion(nuevaPoblacion)
    print('Poblacion: ',poblacion)
    #poblacion=mutacion(poblacion)
    poblacion=elitismo(nuevaPoblacion,list_fitness)
tabla()
print(promedios)
print("Cromosoma óptimo: ", cromosoma_optimo)
print("Función objetivo óptima: ", valor_cromosoma_optimo)