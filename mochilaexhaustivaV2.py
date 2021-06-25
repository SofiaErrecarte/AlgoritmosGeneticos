class Objeto:
    def __init__(self,volumen,valor):
        self.volumen=volumen
        self.valor=valor
        self.utilidad = valor/volumen
    def getVolumen(self):
        return self.volumen
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

#pag 19 pdf
nivel=0
s= [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
voa = -1
soa = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
suma = 0

while (nivel!=-1):
    
    #Generar
    s[nivel] = s[nivel] + 1
    if s[nivel]==1:
        suma=suma+objeto[nivel].volumen
        #Solucion                      ]
    if (nivel==len(s)-1) and (suma<vol_max) and (valor(s)>voa):
        voa=valor(s)
        #print (voa)
        for x in range (0,len(s)):
            soa[x]=s[x]
        #Criterio
    if (nivel<len(s)-1) and (suma<=vol_max):
        nivel = nivel + 1
    else:                   
        while (nivel>-1) and (s[nivel]>=1):
            #Backtracking
            suma=suma-objeto[nivel].volumen*s[nivel]
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
        sumaMochila = sumaMochila + objeto[i].volumen
        #print(objeto[i].volumen)

print("\nTotal Volumen", sumaMochila)
    