import numpy as np
import pandas as pd

ciudades_indice = []
ciudades_distancias = []
list_dire = []
ciudades_recorridas = []   
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

def buscar_minimo(fila_capital):
    mini = 999999
    for i in range(len(fila_capital)):
        if(fila_capital[i] != 0 and fila_capital[i]<mini and fila_capital.index(fila_capital[i]) not in ciudades_indice ): #Chequea que el minimo no sea un 0, que sea menor a min y que no haya pasado ya por la capital                                                                             
            mini = fila_capital[i] #Guardo el nuevo minimo
            indice = fila_capital.index(fila_capital[i]) #Guardo indice
    ciudades_indice.append(indice)
    ciudades_distancias.append(mini)
    ciudades_recorridas.append(nombres_capitales[indice])
    return indice

def heuristica(indice_cap):
    ciudades_indice.append(indice_cap) #Agrego la primera capital a la lista de indices 
    ciudades_recorridas.append(nombres_capitales[indice_cap]) #Agrego el primer nombre a la lista de capitales recorridas
    indice_cap_2 = indice_cap #rebautizo inicializador para usarlo despues
    for i in range(len(nombres_capitales)-1):
        fila_capital = matriz_distancias[indice_cap]
        indice_cap =  buscar_minimo(fila_capital) #busco la capital mas cercana a la capital actual
    ciudades_indice.append(ciudades_indice[0]) #Agregamos la primer capital para que vuelva a origen.
    ciudades_distancias.append(matriz_distancias[ciudades_indice[23]][indice_cap_2]) #Agregamos el recorrido de la ultima capital al origen
    ciudades_recorridas.append(nombres_capitales[indice_cap_2])


cargar_matriz_distancias()
for i in range(len(nombres_capitales)):
        print(i," - ", nombres_capitales[i])
capital_elegida = int(input("Ingrese una capital de partida \n"))
heuristica(capital_elegida)
print(ciudades_recorridas)
print(ciudades_distancias)
print('Recorrido\t'+str(sum(ciudades_distancias)) + 'km')
print('Capital de partida:   ',nombres_capitales[capital_elegida])
print(ciudades_indice)