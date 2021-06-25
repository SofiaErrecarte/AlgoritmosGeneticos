import numpy as np 
class Objeto:
    def __init__(self,gramos,valor):
        self.gramos=gramos
        self.valor=valor
        self.utilidad=valor/gramos
    def getGramos(self):
        return self.gramos
    def getValor(self):
        return self.valor

objeto=[]
objeto.extend([Objeto(1800,72)])
objeto.extend([Objeto(600,36)])
objeto.extend([Objeto(1200,60)])
gramos_max=4200
n=len(objeto)

utilidad_total=0
valor_total=0
gramos_acumulado=0
i=0
mochila=[]
objeto.sort(key=lambda x: x.utilidad, reverse=True)

while (gramos_acumulado<gramos_max) and (i<(n-1)):
    if ((gramos_acumulado+(objeto[i].gramos))<gramos_max):
        mochila.extend([objeto[i]])
        gramos_acumulado += objeto[i].gramos
        valor_total+=objeto[i].valor
        utilidad_total+=objeto[i].utilidad
        i+=1
    else:
        i+=1    
for i in range(len(mochila)):
    print(mochila[i].valor, end=" ")

print("\nGramos de la mochila: ",gramos_acumulado)
print("Valor de la mochila: ",valor_total)