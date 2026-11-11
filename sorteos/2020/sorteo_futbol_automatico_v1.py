# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 22:31:21 2020

@author: alvar
"""
# Este programa solo funciona si los datos se introducen en una misma columna
# en el bloc de notas
# A partir de estos equipos crea eliminatorias o grupos de 4

# Primero vamos a ver cuántos equipos hay en el documento
#nuestro documento está en utf-8, para detectar acentos hay que hacer eso
archivo = open("datos_equipos.txt", "r", encoding="utf-8") 
num_lineas = 0
while True:
    linea = archivo.readline().strip()
    if linea == "":
        break
    else:
        num_lineas += 1
print()
print("El documento tiene", num_lineas, "equipos")
archivo.close()

#Volvemos a abrir para almacenar todos los equipos en varios bombos
#Cada lista es un bombo y todos se engloban dentro de una lista
archivo = open("datos_equipos.txt", "r", encoding="utf-8") 
bombo_n = []   #Contendrá los equipos de cada bombo [BAR, CHE, ...]
bombos = []    #Contendrá las listas de cada bombo  [[BAR, CHE],[ATM, BMU],..]
contador = 0

print()
print("Para sorteo puro,", num_lineas, "equipos en un único bombo")
print("Para eliminatorias con preferencias,", int(num_lineas/2),"equipos en 2 bombos")
equipos_bombo = int(input("Número de equipos en cada bombo: "))
aux = equipos_bombo #para no perder el valor original 
 
while True:
    linea = archivo.readline().strip() #Lee la línea y borra salto de línea
    if linea == "":
        break  #Salimos del bucle cuando se acaban los equipos (linea vacia)
    else:
        if contador < equipos_bombo:
            bombo_n.append(linea)
            contador += 1
        if contador == equipos_bombo and contador <= num_lineas:
            equipos_bombo += aux
            bombos.append(bombo_n) 
            bombo_n = []  #es un bombo provisional, valor se guardó en bombos
        
archivo.close()

# Imprimimos todos los bombos
print()
for i in range(len(bombos)):
    print(bombos[i])
    print()

eliminatorias = input("Son eliminatorias o grupos de 4? (e/g): ")

# Si queremos grupos de 4
if eliminatorias.lower() == "g":
    grupos = []
    #Creamos lista con el número de grupos
    for i in range(int(num_lineas/4)): #convertimos a int porque era float
        grupos.append([])    
    
    # Rellenamos grupos con aleatorios de cada bombo
    from random import choice
    contador = 0
    for i in range(len(bombos)):
            while len(bombos[i]) != 0:
                bolita = choice(bombos[i])
                grupos[contador].append(bolita)
                bombos[i].remove(bolita)
                contador += 1    
                if bombos[i] == []:
                    contador = 0
    #imprimimos de forma bonita
    for i in range(len(grupos)):
        print(grupos[i])
    
# Si queremos eliminatorias
if eliminatorias.lower() == "e":
    # Creamos lista con número de partidos
    partidos = []
    for i in range(int(num_lineas/2)): #convertimos a int porque era float
        partidos.append([]) 
    
    from random import choice
    if len(bombos) == 2:
        contador = 0
        for i in range(len(bombos)): 
            while len(bombos[i]) != 0:
                bolita = choice(bombos[i])
                partidos[contador].append(bolita)
                bombos[i].remove(bolita)
                contador += 1
                if bombos[i] == []:
                    contador = 0
        
    if len(bombos) == 1:
        contador = 0
        while len(bombos[0]) != 0:
            bolita = choice(bombos[0])
            partidos[contador].append(bolita)
            bombos[0].remove(bolita)
            contador += 1
            if contador == int(num_lineas/2):
                contador = 0
    #imprimimos de forma bonita los partidos de eliminatoria
    for i in range(len(partidos)):
        print(partidos[i])