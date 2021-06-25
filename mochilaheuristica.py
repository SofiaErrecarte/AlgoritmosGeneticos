import numpy as np 
class Objeto:
    def __init__(self,volumen,valor):
        self.volumen=volumen
        self.valor=valor
        self.utilidad=valor/volumen
    def getVolumen(self):
        return self.volumen
    def getValor(self):
        return self.valor

objeto=[]
objeto.extend([Objeto(150,20)])
objeto.extend([Objeto(325,40)])
objeto.extend([Objeto(600,50)])
objeto.extend([Objeto(805,36)])
objeto.extend([Objeto(430,25)])
objeto.extend([Objeto(1200,64)])
objeto.extend([Objeto(770,54)])
objeto.extend([Objeto(60,18)])
objeto.extend([Objeto(930,46)])
objeto.extend([Objeto(353,28)])
vol_max=4200
n=len(objeto)

utilidad_total=0
valor_total=0
vol_acumulado=0
i=0
mochila=[]
objeto.sort(key=lambda x: x.utilidad, reverse=True)

while (vol_acumulado<vol_max) and (i<(n-1)):
    if ((vol_acumulado+(objeto[i].volumen))<vol_max):
        mochila.extend([objeto[i]])
        vol_acumulado += objeto[i].volumen
        valor_total+=objeto[i].valor
        utilidad_total+=objeto[i].utilidad
        i+=1
    else:
        i+=1    
for i in range(len(mochila)):
    print(mochila[i].valor, end=" ")

print("\nVolumen de la mochila: ",vol_acumulado)
print("Valor de la mochila: ",valor_total)