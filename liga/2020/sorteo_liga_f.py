# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 22:45:04 2020

@author: alvar
"""


"""
A partir de unos equipos pasados por un archivo de texto el programa debe
devolver un calendario de liga (solo de ida). No debe coincidir ningún 
equipo en cada jornada y no debe repetirse ningún partido
"""



def open_file():
    
    """
    Abre el archivo que contiene a los equipos y nos dice cuántos equipos hay
    en él.
    """
    
    with open("datos_equipos.txt", "r", encoding="utf-8") as archivo:
        num_lineas = 0
        while True:
            linea = archivo.readline().strip()
            if linea == "":
                break
            else:
                num_lineas += 1
        print()
        print("El documento tiene", num_lineas, "equipos")
    
    return num_lineas #número de equipos
    


def team_store(num_lineas):
    
    """
    Abre de nuevo para almacenar todos los equipos en un bombo.
    """

    with open("datos_equipos.txt", "r", encoding="utf-8") as archivo:
        equipos = []    #Contendrá los equipos de la liga  [BAR,CHE,ATM,BMU,..]
        contador = 0
        
        num_equipos = num_lineas
        #aux = num_equipos #para no perder el valor original 
         
        while True:
            linea = archivo.readline().strip() #Lee la línea y borra salto de línea
            if linea == "":
                break  #Salimos del bucle cuando se acaban los equipos (linea vacia)
            else:
                if contador < num_equipos:
                    equipos.append(linea)
                    contador += 1
                    
        # Ordenamos alfabéticamente a los equipos
        equipos.sort()
    
    return equipos, num_equipos
    
    
    
def show_teams(equipos):
    
    """
    Imprime todos los equipos
    """
    
    print()
    print("Equipos en la liga: ")
    for i in range(len(equipos)):
        if i in range(0,9):
            print(i+1," -",equipos[i])
        else:
            print(i+1,"-",equipos[i])
    print()
    

def day_matrix(num_equipos):
    
    """
    Creamos una lista jornadas que contendrá cada una de las jornadas de liga
    cada una de las jornadas será otra lista
    dentro de cada jornada, cada partido será otra lista
    """
    
    num_jornadas = num_equipos - 1 # si 20 equipos, 19 jornadas
    num_partidos = int(num_equipos / 2) #si 20 equipos, 10 partidos cada jornada
    jornadas = []
    for i in range(num_jornadas):
        jornadas.append([])
        for j in range(num_partidos):
            jornadas[i].append([])

    return list(jornadas), num_partidos, num_jornadas
    


def rellenar_jornada(bombo, jor, par, jornadas, num_partidos):
    
    """
    Función que rellena una jornada con partidos aleatorios.
    """
    
    #para la primera jornada
    while len(bombo) != 0 & jor == 0:    
        bolita = choice(bombo)
        jornadas[jor][par].append(bolita)
        bombo.remove(bolita)
        if len(jornadas[jor][par]) == 2: # Si la matriz 'partido' tiene 2 equ:
            par += 1        #pasamos al siguiente partido de la jornada
    
    
    while len(bombo) != 0 & jor != 0:
        
        while par < num_partidos: #intento comparar partidos
            
            if len(jornadas[jor][par]) < 2:
                bolita = choice(bombo)
                jornadas[jor][par].append(bolita)
                bombo.remove(bolita)
            if len(jornadas[jor][par]) == 2:    
                evitar_repeticiones(jornadas, jor, par, equipos)
            par += 1
    
    jor += 1 #preparamos para la siguiente jornada
    par = 0 #preparamos para la siguiente jornada
    
    
    
    
    #debugging...
    for i in range(len(jornadas)):
        print(jornadas[i])
    print("jornada",jor)
    print("partido",par)
    
    
    return jornadas, jor, par
    


def evitar_repeticiones(jornadas, jor, par, equipos, num_partidos):
    
    """
    Rellena cada jornada mirando que no se repita el mismo partido en
    jornadas anteriores
    """
    
    #creamos una copia de jornadas para ordenarla alfabéticamente y que nos
    #sea más fácil comparar las jornadas
    if jor == 0:
        copia_jornadas = deepcopy(jornadas)
        for i in range(len(jornadas)):
            for j in range(2):
                copia_jornadas[i][j].sort() #ordenamos alfabéticamente copia
    
    if jor != 0:
        
        copia_jornadas = deepcopy(jornadas)
        for i in range(len(jornadas)):
            for j in range(2):
                copia_jornadas[i][j].sort() #ordenamos alfabéticamente copia
    
        #miramos a ver si este partido está en jornadas anteriores
    
    print()  #debugging...
    print(copia_jornadas)
    print()
    
    bombo = deepcopy(equipos)   #rellenamos el bombo de nuevo
    rellenar_jornada(bombo, jor, par, jornadas, num_partidos)
    jor+=1
    par=0
    rellenar_jornada(bombo, jor, par, jornadas, num_partidos)

    # if par == num_par: #si es el último partido de la jornada
    #     jor += 1   #pasamos a la siguiente jornada
    #     par = 0     #y pasamos al primer partido de esa jornada
    # print(jornadas) #para chequear cada jornada
    # #si el último partido de la última jornada está completo, vaciamos
    # #bombo para salir del bucle
    # if len(jornadas[num_jornadas-1][num_partidos-1]) == num_partidos:
    #     bombo = []





num_eq = open_file()
(equipos, num_eq) = team_store(num_eq)
show_teams(equipos) #tupla que contiene jornadas, num_par y num_jor

(jornadas, num_par, num_jor) = day_matrix(num_eq)

   
#importamos algunos módulos necesarios
from random import choice

#Todos los equipos deben estar en un bombo del cual extraerlos para cada
# una de las jornadas
#para una copia adecuada de una lista anidada usamos deepcopy
from copy import deepcopy
bombo = deepcopy(equipos) #creo copia equipos, para que no se modifiquen ambas
jor = 0 #va contando las jornadas
par = 0 # va contando los partidos de cada jornada


(jornadas, jor, par) = rellenar_jornada(bombo, jor, par, jornadas, num_par)

evitar_repeticiones(jornadas, jor, par, equipos, num_par)
 
