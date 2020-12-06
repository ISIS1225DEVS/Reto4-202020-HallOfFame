"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config
from DISClib.ADT import list as lt
from App import controller
assert config
from time import process_time
"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


accidentsfile = 'us_accidents_small.csv'
accidentsfile1 = 'us_accidents_dis_2016.csv'
accidentsfile2 = 'us_accidents_dis_2017.csv'
accidentsfile3 = 'us_accidents_dis_2018.csv'
accidentsfile4 = 'us_accidents_dis_2019.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Requerimento 1")
    print("4- Requerimento 2")
    print("5- Requerimento 3")
    print("6- Requerimento 4")
    print("7- Requerimento 5")
    print("8- Requerimento 8")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()
        print("\nInicializado....")

    elif int(inputs[0]) == 2:
        print("\nCargando información de accidentes ....")
        t1_start = process_time() #tiempo inicial
        controller.loadData(cont,accidentsfile)
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos ")
        print('Accidentes cargados: ' + str(controller.accisSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))

    elif int(inputs[0]) == 3:
        print("\nRequerimiento No 1 del reto 3: ")
        LaDate = input("Fecha (YYYY-MM-DD): ")
        controller.getAccisByRangeSev(cont, LaDate)
        
    elif int(inputs[0]) == 4:
        print("\nRequerimiento No 2 del reto 3: ")
        LaDate = input("Fecha (YYYY-MM-DD): ")
        controller.getAccidentsLess(cont, LaDate)

    elif int(inputs[0]) == 5:
        print("\nRequerimiento No 3 del reto 3: ")
        LaDate = input("Fecha inicio (YYYY-MM-DD): ")
        LaDate1 = input("Fecha final (YYYY-MM-DD): ")
        controller.getAccidentsCategory( cont , LaDate, LaDate1)
        
    elif int(inputs[0]) == 6:
        print("\nRequerimiento No 4 del reto 3: ")
        LaDate = input("Fecha inicio (YYYY-MM-DD): ")
        LaDate1 = input("Fecha final (YYYY-MM-DD): ")
        controller.getAccidentsState( cont , LaDate, LaDate1)

    elif int(inputs[0]) == 7:
        print("\nRequerimiento No 5 del reto 3: ")
        LaDate = input("Hora inicio (hh:mm): ")
        LaDate1 = input("Hora final (hh:mm): ")
        controller.getAccidentsHour( cont , LaDate, LaDate1)

    elif int(inputs[0]) == 8:
        print("\nBono 1 del reto 3: ")
        lat = input("latitud: ")
        lon = input("longitud: ")
        rad = input("radio en millas: ")
        controller.getradius(cont, lon,lat,rad)

    else:
        sys.exit(0)
sys.exit(0)
