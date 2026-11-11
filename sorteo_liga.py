# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 15:34:25 2020

@author: alvar
"""

# A partir de unos equipos pasados por un archivo de texto el programa debe
# devolver un calendario de liga (solo de ida). No debe coincidir ningún 
# equipo en cada jornada y no debe repetirse ningún partido

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

#Volvemos a abrir para almacenar todos los equipos en un bombo
archivo = open("datos_equipos.txt", "r", encoding="utf-8") 
equipos = []    #Contendrá los equipos de la liga  [BAR,CHE,ATM,BMU,..]
contador = 0

num_equipos = num_lineas
aux = num_equipos #para no perder el valor original 
 
while True:
    linea = archivo.readline().strip() #Lee la línea y borra salto de línea
    if linea == "":
        break  #Salimos del bucle cuando se acaban los equipos (linea vacia)
    else:
        if contador < num_equipos:
            equipos.append(linea)
            contador += 1
        
archivo.close()

# Ordenamos alfabéticamente a los equipos
equipos.sort()

# Imprimimos todos los equipos
print()
print("Equipos en la liga: ")
for i in range(len(equipos)):
    if i in range(0,9):
        print(i+1," -",equipos[i])
    else:
        print(i+1,"-",equipos[i])

# Creamos una lista jornadas que contendrá cada una de las jornadas de liga
# cada una de las jornadas será otra lista
# dentro de cada jornada, cada partido será otra lista
num_jornadas = num_equipos - 1 # si 20 equipos, 19 jornadas
num_partidos = int(num_equipos / 2) #si 20 equipos, 10 partidos cada jornada
jornadas = []
for i in range(num_jornadas):
    jornadas.append([])
    for j in range(num_partidos):
        jornadas[i].append([])


# Un posible bucle empezaría desde aqui (borrar comentario)
#Todos los equipos deben estar en un bombo del cual extraerlos para cada
# una de las jornadas
#para una copia adecuada de una lista anidada usamos deepcopy
from copy import deepcopy
bombo = deepcopy(equipos) #creo copia equipos, para que no se modifiquen ambas
jor = 0 #va contando las jornadas
par = 0 # va contando los partidos de cada jornada

from random import choice

# Con esto rellenamos las jornadas con partidos aleatorios
# De momento no ha sido posible que no se repitan partidos
while len(bombo) != 0:
    if jor == 0:    #la primera jornada no puede compararse con la anterior    
            bolita = choice(bombo)
            jornadas[jor][par].append(bolita)
            bombo.remove(bolita)
            if len(jornadas[jor][par]) == 2: # Si la matriz 'partido' tiene 2 equ:
                par += 1        #pasamos al siguiente partido de la jornada
            if par == num_partidos: #si es el último partido de la jornada
                jor += 1   #pasamos a la siguiente jornada
                par = 0     #y pasamos al primer partido de esa jornadaa
                bombo = deepcopy(equipos)   #y rellenamos el bombo de nuevo
                print(jornadas) #para chequear cada jornada
            #si el último partido de la última jornada está completo, vaciamos
            #bombo para salir del bucle
            if len(jornadas[num_jornadas-1][num_partidos-1]) == num_partidos:
                bombo = []
    #intentamos que no se repita
    if jor != 0:
        bolita = choice(bombo)
        jornadas[jor][par].append(bolita)
        bombo.remove(bolita)
        if len(jornadas[jor][par]) == 2:    
            for i in range(jor):
                for j in range(num_partidos):
                    print(i,j) #para ver dónde va
                    
                    if len(jornadas[jor][par]) == 2:  
                        if (jornadas[jor][par][0] in jornadas[i][j]
                            and jornadas[jor][par][1] in jornadas[i][j]):
                            bombo.append(bolita)    
                            jornadas[i][j].remove(bolita)
                        elif (jornadas[jor][par][0] not in jornadas[i][j]
                            or jornadas[jor][par][1] not in jornadas[i][j]):
                                if par < num_partidos:    
                                    par += 1
                                elif par == num_partidos:
                                    jor += 1
                                    par = 0
                     
        if par == num_partidos: #si es el último partido de la jornada
                jor += 1   #pasamos a la siguiente jornada
                par = 0     #y pasamos al primer partido de esa jornadaa
                bombo = deepcopy(equipos)   #y rellenamos el bombo de nuevo
                print(jornadas) #para chequear cada jornada
            #si el último partido de la última jornada está completo, vaciamos
            #bombo para salir del bucle
        if len(jornadas[num_jornadas-1][num_partidos-1]) == num_partidos:
                bombo = []
                        
        #PARECE QUE HAY UN FALLO EN EL MOMENTO EN EL QUE SE REPITE EL EQUIPO
        #LA PRIMERA JORNADA SALE SIN PROBLEMAS PERO LUEGO SE MODIFICA
print(jornadas)
