
class Objeto():
    def __init__(self,volumen,valor):
        self.volumen=volumen
        self.valor= valor
    def getVolumen(self):
        return self.volumen
    def getValor(self):
        return self.valor

#armar la lista con los objetos
objetos=[]
objetos.extend([Objeto(150,20)])
objetos.extend([Objeto(325,40)])
objetos.extend([Objeto(600,50)])
objetos.extend([Objeto(805,36)])
objetos.extend([Objeto(430,25)])
objetos.extend([Objeto(1200,64)])
objetos.extend([Objeto(770,54)])
objetos.extend([Objeto(60,18)])
objetos.extend([Objeto(930,46)])
objetos.extend([Objeto(353,28)])

#hacer un arrar de 1024 posiciones, lo inicializo con 0
combinaciones =  [0 for columna in range(0,1024)] 

#  0 significa que ese objeto no va en la mochila y 1 significa que ese objeto si va en la mochila
datos=['1','0']
# combinaciones son en total 10 elementos posibles
cont=0
for a in range (len(datos)):
    for b in range(len(datos)):
        for c in range(len(datos)):
            for d in range(len(datos)):
                for e in range(len(datos)):
                    for f in range(len(datos)):
                        for g in range(len(datos)):
                            for h in range(len(datos)):
                                for i in range(len(datos)):
                                    for j in range(len(datos)):
                                        combinaciones[cont]=datos[a]+datos[b]+datos[c]+datos[d]+datos[e]+datos[f]+datos[g]+datos[h]+datos[i]+datos[j]
                                        cont=cont + 1
#imprimo todas las combinaciones y el contador para verificar
#for x in range(len(combinaciones)):
    #print(combinaciones[x])
    #print('\n')
#print(cont)


mejorCombinacionMochila=0
mejorValorMochila=0
maximoVolumen=4200  #creo que era este el valor
#comparo cada combinacion de mochila
for x in range(len(combinaciones)):
    volumenTotal=0
    valorTotal=0
    for j in range(len(combinaciones[x])):
        #calculo el peso total y valor total de la mochila
        if(combinaciones[x][j]=='1'):
            volumenTotal=volumenTotal+objetos[j].volumen
            #print(volumenTotal)
            valorTotal=valorTotal+objetos[j].valor
            #print(valorTotal)
            #print(volumenTotal)
       
        #me fijo si el peso de esa mochila supera el maximo
        #si no supera calculo la funcion y busco el maximo 

        #hago la validacion que volumenTotal != 0 ya que la combinacion [0,0,0,0,0,0,0,0,0,0] 
        # me da volumen y valor =0 y no se puede dividir por 0
        
    if(volumenTotal<=maximoVolumen):
        #print(volumenTotal)
        comb=combinaciones[x]
        #print(comb)
        
        #print(totalvalor)
        #print(funcion)
        if(valorTotal>=mejorValorMochila):
            mejorValorMochila=valorTotal
            mejorCombinacionMochila=combinaciones[x]

mejorCombinacionMochila=str(mejorCombinacionMochila)
mejor_combinacion = [int(i) for i in list(mejorCombinacionMochila)]

print(mejor_combinacion) #en 0 y 1
print("Valores de la mochila:")
for i in range (len(mejor_combinacion)):
    if(mejor_combinacion[i]==1):
        print(objetos[i].valor,end=" ")
print("\nVolumenes de la mochila:")
for i in range (len(mejor_combinacion)):
    if(mejor_combinacion[i]==1):
        print(objetos[i].volumen,end=" ")
sumaMochila =0
for i in range(len(mejor_combinacion)):
    if(mejor_combinacion[i]==1):
        sumaMochila = sumaMochila + objetos[i].volumen
        #print(objeto[i].volumen)

print("\nTotal $",mejorValorMochila)
print("Total Volumen", sumaMochila)