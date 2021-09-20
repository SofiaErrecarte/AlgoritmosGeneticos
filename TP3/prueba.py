nombres_capitales = [
    "Ciudad de Buenos Aires",    "Córdoba",    "Corrientes",    "Formosa",    "La Plata",    "La Rioja",    "Mendoza",    "Neuquen",
    "Paraná",    "Posadas",    "Rawson",    "Resistencia",    "Río Gallegos",    "San Fernando del Valle de Catamarca",
    "San Miguel de Tucumán",    "San Salvador de Jujuy",    "Salta",    "San Juan",    "San Luis",    "Santa Fe",    "Santa Rosa",
    "Santiago del Estero",    "Ushuaia",    "Viedma"]
nombres_mejor=[]
mejor_recorrido=[11, 20, 12, 22, 10, 5, 13, 8, 4, 19, 0, 7, 23, 9, 14, 1, 15, 2, 16, 6, 17, 18, 3, 21, 11]
for i in range(25):
    nombres_mejor.append(nombres_capitales[mejor_recorrido[i]])
print(nombres_mejor)