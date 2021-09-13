import numpy as np
from numpy.core.fromnumeric import argsort
from numpy.lib.function_base import append
import pandas as pd
import openpyxl
import random as rand
import os

#os.system('cls')
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
listaNumeros = np.arange(0,24)
cantPoblacionInicial=50
prob_crossover=0.75
prob_mutacion=0.05
ciclos=200
ruta= "C:\\Users\\Usuario\\Desktop\\Tabla.xlsx"

def cargar_matriz_distancias():
    data = pd.read_excel('C:\\Users\\Usuario\\Desktop\\TablaCapitales.xlsx') 
    for i in range(24):
        matriz_distancias.append([])
        for j in range(24):
            matriz_distancias[i].append(data.iloc[i, j+1])  #me paro en cada fila (i) , columna(j) - el iloc es para ubicar una celda                                           
            if (np.isnan(matriz_distancias[i][j]) == True): #busco el vacio de la diagonal principal y le pongo valor cero
                matriz_distancias[j][j] = 0

def buscar_minimo(fila_capital):
    mini = 999999 #en la primer iteracion la primera que encuentra ya esta 
    for i in range(len(fila_capital)):
        if(fila_capital[i] != 0 and fila_capital[i]<mini and fila_capital.index(fila_capital[i]) not in ciudades_indice ): #Chequea que el minimo no sea un 0, que sea menor a min y que no haya pasado ya por la capital                                                                             
            mini = fila_capital[i] #Guardo la distancia minima nueva de la capital 
            indice = fila_capital.index(fila_capital[i]) #Guardo indice minimo actual
    ciudades_indice.append(indice)
    ciudades_distancias.append(mini)
    ciudades_recorridas.append(nombres_capitales[indice])
    return indice

def heuristica(indice_cap):
    ciudades_indice.append(indice_cap) #Agrego la primera capital a la lista de indices 
    ciudades_recorridas.append(nombres_capitales[indice_cap]) #Agrego el primer nombre a la lista de capitales recorridas
    indice_cap_inicial = indice_cap #para poder asignarlo como ultima ciudad
    for i in range(len(nombres_capitales)-1):
        fila_capital = matriz_distancias[indice_cap]
        indice_cap =  buscar_minimo(fila_capital) #busco el indice de la capital mas cercana a la capital actual
    ciudades_indice.append(ciudades_indice[0]) #Agregamos la primer capital para que vuelva a origen.
    ciudades_distancias.append(matriz_distancias[ciudades_indice[23]][indice_cap_inicial]) #Agregamos el recorrido de la ultima capital al origen
    ciudades_recorridas.append(nombres_capitales[indice_cap_inicial])

def crearPoblacionInicial():    
    poblacion = []
    for i in range(cantPoblacionInicial):
        poblacion.append(rand.sample(list(listaNumeros), 24))
        poblacion[i].append(poblacion[i][0])   
    return poblacion

def calcularFuncionObjetivo(poblacion):
    funcion_obj=list(np.zeros(cantPoblacionInicial))
    for i in range(cantPoblacionInicial):
        suma = 0
        for j in range (len(poblacion[i])-1):
            suma += matriz_distancias[poblacion[i][j]][poblacion[i][j+1]]
        #suma+=matriz_distancias[poblacion[i][j+1]][poblacion[i][0]] #esta la agrego por vuelve a ciu de inicio
        funcion_obj[i] = suma
    return funcion_obj

def calcularFitness(funcion_obj):
    list_fitness=list(np.zeros(cantPoblacionInicial))
    sumatoria = sum(funcion_obj)
    for i in range(cantPoblacionInicial):                          
        list_fitness[i] = (1 - (funcion_obj[i]/sumatoria))
    return list_fitness

def crearRuleta(list_fitness):
    nuevoFitness = list(np.zeros(cantPoblacionInicial))
    sumaFitness = sum(list_fitness)
    for i in range(len(list_fitness)):
        nuevoFitness[i] = (list_fitness[i]/sumaFitness)
    fitnes_acum = []
    fitnes_acum.append(nuevoFitness[0])
    for i in range(1,cantPoblacionInicial):
        acumulado = fitnes_acum[i - 1] + nuevoFitness[i]
        fitnes_acum.append(acumulado)
    #print(fitnes_acum)
    return fitnes_acum

def crearRango (list_fitness,poblacion):
    rango=[]
    mejores_fitness=[]
    indices= list(np.argsort(list_fitness)) #Ordeno los indices de menor a mayor y los hago lista para recorrerlos
    #print(indices)
    for i in range(16,len(indices)): #Me quedo con los 24 mejores
        mejores_fitness.append(indices[i])
    for i in range(len(mejores_fitness)): #agrego los 24 mejores a la población
        rango.append(poblacion[i])
    return rango

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

def crossover_rango(list_fitness,poblacion):
    hijos = []
    rango=crearRango(list_fitness,poblacion)
    for i in range(len(rango)):
        hijos.append(rango[i])
    #print('RULETA: ',ruleta)
    
    for i in range (0,16,2):#16 son los que reemplazo por crossover entre los 24 elegidos 
        padre_1 = rand.choice(rango)
        padre_2 = rand.choice(rango)
        if (rand.random() <= prob_crossover):
            padre_1,padre_2=crossoverCiclico(padre_1,padre_2)
        hijos.append(padre_1)
        hijos.append(padre_2)
    return hijos

def elegir_ruleta(ruleta,poblacion):
    padres = []
    for _ in range(2):
        frec = rand.uniform(0,1)
        for i in range(cantPoblacionInicial):
            if(ruleta[i] > frec):
                poblacion[i].pop() #Le quito el ultimo que seria la misma cap donde arranca
                padres.append(poblacion[i])  #Agrego como padre elegido esa poblacion sin esa ultima capital
                poblacion[i].append(poblacion[i][0])  #le vuelvo a setear esa capital al final a la poblacion inicial   
                break
    return padres[0], padres[1]

def crossover(list_fitness,poblacion):
    ruleta=crearRuleta(list_fitness)
    aux=np.array(funcion_obj)
    min1 = aux.argsort()[0]
    min2 = aux.argsort()[1]
    aux = list(aux)
    aux[0] = poblacion[min1]
    aux[1] = poblacion[min2]
    for i in range (2,len(poblacion)-1,2):
        padre_1,padre_2 = elegir_ruleta(ruleta,poblacion) 
        padre_1,padre_2=crossoverCiclico(padre_1,padre_2)
        aux[i]=padre_1
        aux[i + 1]= padre_2
        #hijos[i] = padre_1
        #hijos[i + 1]= padre_2
    #print('hijos', hijos)
    return aux

def crossover_elitismo(list_fitness,poblacion):
    #Tomo los 10 cromosomas con mejores fitnes y los mantengo
    #print(list_fitness)
    hijos = []
    mejores_fitness=[]
    indices= list(np.argsort(list_fitness)) #Ordeno los indices de menor a mayor y los hago lista para recorrerlos
    #print(indices)
    for i in range(40,len(indices)): #Me quedo con los 10 mejores
        mejores_fitness.append(indices[i])
    #print(mejores_fitness)
    ruleta=crearRuleta(list_fitness)
    for i in range(len(mejores_fitness)): #agrego los 10 mejores a la población
        hijos.append(poblacion[i])
    #print(hijos)
    for i in range (0,len(poblacion)-1-10,2):
        padre_1,padre_2 = elegir_ruleta(ruleta,poblacion)
        #print('Padre1',padre_1)
        #print('Padre2',padre_2)        
        #padre_1 = rand.choice(ruleta)
        #padre_2 = rand.choice(ruleta)
        #if (rand.random() <= prob_crossover):
        padre_1,padre_2=crossoverCiclico(padre_1,padre_2)
        hijos.append(padre_1)
        hijos.append(padre_2)
    return hijos

def mutacion(poblacion):
    for i in range(len(poblacion)):  
        x = rand.uniform(0,1)
        if(x<=prob_mutacion):
            aleat_1 = rand.randrange(0,23)
            aleat_2 = rand.randrange(0,23)
            while(aleat_2 == aleat_1):
                aleat_2 = rand.randrange(0,23)
            aux = poblacion[i][aleat_1]
            poblacion[i][aleat_1] = poblacion[i][aleat_2]
            poblacion[i][aleat_2] = aux
    return poblacion

def tabla(op):
    lista_excel = []
    lista_excel.append(list(range(1,ciclos+1)))
    lista_excel.append(maximos)
    lista_excel.append(minimos)
    lista_excel.append(promedios)
    lista_excel.append(lista_optimo)
    df=pd.DataFrame(lista_excel)
    df = df.T
    df.columns = ['Corrida','Maximo FO','Minimo FO','Promedio FO','Lista Optimo']
    tabla = pd.ExcelWriter(ruta, engine='xlsxwriter') 
    if (op==3):
        df.to_excel(tabla, sheet_name='Geneticos', index = False)     
        workbook = tabla.book
        worksheet = tabla.sheets["Geneticos"] 
        formato = workbook.add_format({"align": "center"})

        worksheet.set_column("A:D", 15, formato)  
        worksheet.conditional_format("D1:DF"+str(len(promedios)+1), {"type": "3_color_scale", "max_color": "red", "mid_color": "yellow", "min_color": "green"})

    elif(op==4):
        df.to_excel(tabla, sheet_name='Geneticos elite', index = False)     
        workbook = tabla.book
        worksheet = tabla.sheets["Geneticos elite"] 
        formato = workbook.add_format({"align": "center"})

        worksheet.set_column("A:D", 15, formato)  
        worksheet.conditional_format("D1:DF"+str(len(promedios)+1), {"type": "3_color_scale", "max_color": "red", "mid_color": "yellow", "min_color": "green"})

    elif(op==5):
        df.to_excel(tabla, sheet_name='Rango', index = False)     
        workbook = tabla.book
        worksheet = tabla.sheets["Rango"] 
        formato = workbook.add_format({"align": "center"})

        worksheet.set_column("A:D", 15, formato)  
        worksheet.conditional_format("D1:DF"+str(len(promedios)+1), {"type": "3_color_scale", "max_color": "red", "mid_color": "yellow", "min_color": "green"})

    tabla.save()


#reemplazo 16 me quedo con 24
cargar_matriz_distancias()
ciudades_indice = []
ciudades_distancias = []
ciudades_recorridas = []
distancias= []
recorridos=[]
ciudades_recorridas = []

#MENU
print('1. Heuristica con capital \n2.Mejor Heuristica \n3.Algoritmo Genético con ruleta \n4.Algoritmo Genético con Elite \n5.Algoritmo Genético con rango \n6.Salir')
op= int(input("Ingrese una opcion del menú \n"))
while(op!=6):
    if(op==1): #elección de heuristica con capital
        ciudades_indice = []
        ciudades_distancias = []
        ciudades_recorridas = []
        ciudades_recorridas = []
        for i in range(len(nombres_capitales)):
            print(i," - ", nombres_capitales[i])
        capital_elegida = int(input("Ingrese una capital de partida \n"))
        heuristica(capital_elegida)
        print(ciudades_recorridas)
        print(ciudades_distancias)
        print('Recorrido\t'+str(sum(ciudades_distancias)) + 'km')
        print('Capital de partida:   ',nombres_capitales[capital_elegida])
        print(ciudades_indice)
        print('1.Heuristica con capital \n2.Mejor Heuristica \n3.Algoritmo Genético \n4.Algoritmo Genético con Elite \n5.Algoritmo Genético con rango \n6.Salir')
        op= int(input("Ingrese una opcion del menú \n"))
    if(op==2):#elección de heuristica general
        ciudades_indice = []
        ciudades_distancias = []
        distancias= []
        recorridos=[]
        for i in range(len(nombres_capitales)):
            heuristica(i)
            distancias.append(sum(ciudades_distancias)) #Guarda la sumatoria de los recorridos minimos.
            recorridos.append(ciudades_indice) #Guardo los recorridos partiendo de cada capital
            ciudades_indice = [] #Sobreescribo las listas para cada iteración del bucle.
            ciudades_distancias = []
        for i in range(len(distancias)):
            print(distancias[i])
        for i in range(len(recorridos)):
            print(recorridos[i])
        for i in range(len(distancias)):
            if(distancias[i] == min(distancias)):
                indice_mejor = i
        print('recorrido: ',recorridos[indice_mejor])
        print('mejor: ',min(distancias))
        print('capital: ', nombres_capitales[indice_mejor])
        print('1. Heuristica con capital \n2.Mejor Heuristica \n3.Algoritmo Genético \n4.Algoritmo Genético con Elite \n5.Algoritmo Genético con rango \n6.Salir')
        op= int(input("Ingrese una opcion del menú \n"))
    if(op==3):
        poblacion=crearPoblacionInicial()
        funcion_obj= calcularFuncionObjetivo(poblacion)
        list_fitness= calcularFitness(funcion_obj)
        promedios=[]
        maximos=[]
        minimos=[]
        lista_optimo=[]
        valor_cromosoma_optimo = 0
        cromosoma_optimo = []
        for x in range (ciclos):
            minimoObj = min(funcion_obj)
            minimos.append(minimoObj)
            maximos.append(max(funcion_obj))
            promedios.append(np.mean(funcion_obj))
            indice = funcion_obj.index(minimoObj)
            optimo = poblacion[indice]
            lista_optimo.append(optimo)
            if (minimoObj < valor_cromosoma_optimo) or (valor_cromosoma_optimo == 0):
                valor_cromosoma_optimo = minimoObj
                cromosoma_optimo = optimo
            poblacion=crossover(list_fitness,poblacion)
            #poblacion = mutacion(poblacion)
            print(poblacion)
            funcion_obj= calcularFuncionObjetivo(poblacion)
            list_fitness= calcularFitness(funcion_obj)
        tabla(3)
        print("Cromosoma óptimo: ", cromosoma_optimo)
        print("Función objetivo óptima: ", valor_cromosoma_optimo)
        print('1. Heuristica con capital \n2.Mejor Heuristica \n3.Algoritmo Genético \n4.Algoritmo Genético con Elite \n5.Algoritmo Genético con rango \n6.Salir')
        op= int(input("Ingrese una opcion del menú \n"))
    if(op==4):
        promedios=[]
        maximos=[]
        minimos=[]
        lista_optimo=[]
        valor_cromosoma_optimo = 0
        cromosoma_optimo = []
        poblacion=crearPoblacionInicial()
        funcion_obj= calcularFuncionObjetivo(poblacion)
        list_fitness= calcularFitness(funcion_obj)
        for x in range (ciclos):
            minimoObj = min(funcion_obj)
            minimos.append(minimoObj)
            promedios.append(np.mean(funcion_obj))
            indice = funcion_obj.index(minimoObj)
            optimo = poblacion[indice]
            lista_optimo.append(optimo)
            if (minimoObj < valor_cromosoma_optimo) or (valor_cromosoma_optimo == 0):
                valor_cromosoma_optimo = minimoObj
                cromosoma_optimo = optimo
            poblacion=crossover_elitismo(list_fitness,poblacion)
            poblacion = mutacion(poblacion)
            funcion_obj= calcularFuncionObjetivo(poblacion)
            list_fitness= calcularFitness(funcion_obj)
        tabla(4)
        print("Cromosoma óptimo: ", cromosoma_optimo)
        print("Función objetivo óptima: ", valor_cromosoma_optimo)
        print('1. Heuristica con capital \n2.Mejor Heuristica \n3.Algoritmo Genético \n4.Algoritmo Genético con Elite \n5.Algoritmo Genético con rango \n6.Salir')
        op= int(input("Ingrese una opcion del menú \n"))
    if(op==5):
        promedios=[]
        maximos=[]
        minimos=[]
        lista_optimo=[]
        valor_cromosoma_optimo = 0
        cromosoma_optimo = []
        poblacion=crearPoblacionInicial()
        funcion_obj= calcularFuncionObjetivo(poblacion)
        list_fitness= calcularFitness(funcion_obj)
        for x in range (ciclos):
            minimoObj = min(funcion_obj)
            minimos.append(minimoObj)
            promedios.append(np.mean(funcion_obj))
            indice = funcion_obj.index(minimoObj)
            optimo = poblacion[indice]
            lista_optimo.append(optimo)
            if (minimoObj < valor_cromosoma_optimo) or (valor_cromosoma_optimo == 0):
                valor_cromosoma_optimo = minimoObj
                cromosoma_optimo = optimo
            poblacion=crossover_rango(list_fitness,poblacion)
            poblacion = mutacion(poblacion)
            funcion_obj= calcularFuncionObjetivo(poblacion)
            list_fitness= calcularFitness(funcion_obj)
        tabla(5)
        print("Cromosoma óptimo: ", cromosoma_optimo)
        print("Función objetivo óptima: ", valor_cromosoma_optimo)
        print('1. Heuristica con capital \n2.Mejor Heuristica \n3.Algoritmo Genético \n4.Algoritmo Genético con Elite \n5.Algoritmo Genético con rango \n6.Salir')
        op= int(input("Ingrese una opcion del menú \n"))

        
