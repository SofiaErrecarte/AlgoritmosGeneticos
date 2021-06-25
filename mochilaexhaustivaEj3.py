class Objeto:
    def __init__(self,gramos,valor):
        self.gramos=gramos
        self.valor=valor
        self.utilidad = valor/gramos
    def getGramos(self):
        return self.gramos
    def getValor(self):
        return self.valor
    def GetUtilidad(self):
        return self.utilidad

def valor (s):
    suma=0
    for x in range (0, len (s)):
        if s[x]==1:
            suma=suma+objeto[x].valor
    return suma

objeto=[]
objeto.extend([Objeto(1800,72)])
objeto.extend([Objeto(600,36)])
objeto.extend([Objeto(1200,60)])
gramos_max=3000

#pag 19 pdf
nivel=0
s= [-1,-1,-1]
voa = -1
soa = [-1,-1,-1]
suma = 0

while (nivel!=-1):
    
    #Generar
    s[nivel] = s[nivel] + 1
    if s[nivel]==1:
        suma=suma+objeto[nivel].gramos
        #Solucion                      
    if (nivel==len(s)-1) and (suma<gramos_max) and (valor(s)>voa):
        voa=valor(s)
        #print (voa)
        for x in range (0,len(s)):
            soa[x]=s[x]
        #Criterio
    if (nivel<len(s)-1) and (suma<=gramos_max):
        nivel = nivel + 1
    else:                   
        while (nivel>-1) and (s[nivel]>=1):
            #Backtracking
            suma=suma-objeto[nivel].gramos*s[nivel]
            s[nivel]=-1
            nivel=nivel-1

    
print(soa)
print("Objetos: ")
for i in range (len(soa)):
    if(soa[i]==1):
        print(objeto[i].valor,end=" ")
sumaMochila =0
for i in range(len(soa)):
    if(soa[i]==1):
        sumaMochila = sumaMochila + objeto[i].gramos
        #print(objeto[i].gramos)

print("\nTotal Gramos", sumaMochila)
    