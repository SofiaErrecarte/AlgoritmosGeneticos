from typing import runtime_checkable
import numpy as np
import random as rand
from numpy.core.numeric import zeros_like
import pandas as pd
import plotly.express as px

cant_poblacion = 50
listaNumeros = np.arange(0,24)
matriz_distancias = []
prob_mutacion= 0.03
prob_crossover=0.75
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

direct_capitales = [[85,75],[6,130],[87,195],[96,218],[93,69],[-35,163],[-61,103],[-46,0],[59,124],
[133,195],[-3,-74],[85,195],[-39,-220],[-17,181],[-11,211],[-13,252],[-14,243],[-59,128],[-26,99],
[57,125],[7,43],[4,191],[-29,-270],[21,-30]] #Direcciones X e Y en el mapa politico de ARG


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
        poblacion.append(rand.sample(list(listaNumeros), 24)) #crea una lista random de 0 a 24
        poblacion[i].append(poblacion[i][0]) #agrega la capital inicial al final        
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
    return hijo1,hijo2

def crossover(poblacion,list_fitness):
    ruleta = crear_ruleta(list_fitness)
    x = rand.uniform(0,1)
    nuevaPoblacion = []
    i = 0
    for _ in range(25): 
        if(x<=prob_crossover):
            ind1 = ruleta[i]
            ind2 = ruleta[i+1]        
            reco1 = poblacion[ind1]
            reco2 = poblacion[ind2] 
            padre1,padre2=crossoverCiclico(reco1,reco2)
            nuevaPoblacion.append(padre1)
            nuevaPoblacion.append(padre2)
            i+=2
        elif(x>prob_crossover):
            nuevaPoblacion.append(poblacion[i])
            nuevaPoblacion.append(poblacion[i+1])
            i+=2
    #print(len(nuevaPoblacion))
    return nuevaPoblacion

def elite(poblacion,list_fitness):
    ruleta = crear_ruleta(list_fitness)
    nuevaPoblacion = []
    indices = np.array(funcion_obj)
    indices=indices.argsort() 
    for i in range(10):
        j=indices[i]
        nuevaPoblacion.append(poblacion[j])
    for i in range(10):
        print(nuevaPoblacion[i])
    x = rand.uniform(0,1)
    i = 0
    for _ in range(20): 
        if(x<=prob_crossover):
            ind1 = ruleta[i]
            ind2 = ruleta[i+1]        
            reco1 = poblacion[ind1]
            reco2 = poblacion[ind2] 
            padre1,padre2=crossoverCiclico(reco1,reco2)
            nuevaPoblacion.append(padre1)
            nuevaPoblacion.append(padre2)
            i+=2
        elif(x>prob_crossover):
            nuevaPoblacion.append(poblacion[i])
            nuevaPoblacion.append(poblacion[i+1])
            i+=2
    return nuevaPoblacion

def mutacion(poblacion):
    x=rand.random()
    for i in range(50):
        if(x <= prob_mutacion):
            r1 = rand.randrange(0,23)
            r2 = rand.randrange(0,23)
            while(r1==r2):
                r1=rand.randrange(0,23)
            aux = poblacion[i][r1]
            poblacion[i][r1] = poblacion[i][r2]
            poblacion[i][r2] = aux
    return poblacion

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

def crossover_rango(list_fitness,poblacion):
    nuevaPoblacion = []
    rango=[]
    print(list_fitness)
    indices = np.array(list_fitness)
    indices=indices.argsort() 
    print(indices)
    for i in range(20,50):
        j=indices[i]
        rango.append(poblacion[j])
    '''for i in range(30):
        print(nuevaPoblacion[i])'''
    for i in range(30):
        nuevaPoblacion.append(rango[i])
    print('poblacion ',nuevaPoblacion)
    for i in range (0,20,2):#20 son los que reemplazo por crossover entre los 30 elegidos 
        padre_1 = rand.choice(rango)
        padre_2 = rand.choice(rango)
        if (rand.random() <= prob_crossover):
            padre_1,padre_2=crossoverCiclico(padre_1,padre_2)
        nuevaPoblacion.append(padre_1)
        nuevaPoblacion.append(padre_2)
    for i in range(30):
        nuevaPoblacion.append(rango[i])
    print('nueva ',nuevaPoblacion)
    return nuevaPoblacion

def imprime_mapa(cromosoma_optimo):
    listaOrdenada = []
    dfCapitales = pd.read_csv("C:\\Users\\Usuario\\Desktop\\provincias.csv")
    listaCapitales = dfCapitales.values.tolist()
    for i in cromosoma_optimo:
        listaOrdenada.append(listaCapitales[i])
        fig = px.line_mapbox(listaOrdenada, lat=1, lon=2, zoom=3, width=1000,height=900)
        fig.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=3.8, mapbox_center_lat = -40,margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()
    
cargaMatrizDeDistancias()
poblacion= crear_poblacion()
#print('Poblacion inicial: ',poblacion)
for i in range(ciclos):
    funcion_obj = calcular_funcion_objetivo(poblacion)
    list_fitness = calcular_fitness(funcion_obj)
    dist_min = min(funcion_obj)
    minimos.append(dist_min)
    maximos.append(max(funcion_obj))
    promedios.append(np.mean(funcion_obj))
    indice = funcion_obj.index(dist_min)
    optimo = poblacion[indice]
    optimos.append(optimo)
    if (dist_min < valor_cromosoma_optimo) or (valor_cromosoma_optimo == 0):
        valor_cromosoma_optimo = dist_min
        cromosoma_optimo = optimo
    poblacion=crossover(poblacion,list_fitness)
    #poblacion=elite(poblacion,list_fitness)
    #poblacion=crossover_rango(list_fitness,poblacion)
    poblacion=mutacion(poblacion)

imprime_mapa(cromosoma_optimo)
tabla()
print(promedios)
print("Cromosoma óptimo: ", cromosoma_optimo)
print("Función objetivo óptima: ", valor_cromosoma_optimo)