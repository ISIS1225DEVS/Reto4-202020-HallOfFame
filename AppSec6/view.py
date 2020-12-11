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
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from App import controller
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

citibike_file ='Reto4-202020-Template\\Data'
#'201801-1-citibike-tripdata.csv'
'Reto4-202020-Template\\Data'
initialStation = None
recursionLimit = 20000
# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de citibike")
    print("3- Requerimiento 1 ")
    print("4- Requerimiento 2 ")
    print("5- Requerimiento 3")
    print("6- Requerimiento 5")
    print("7- Requerimiento 6")
    print("0- Salir")
    print("*******************************************")

def optionTwo():
    print("\nCargando información de Citibike ....")
    controller. loadTrips(cont)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))


def optionThree():
    print("Requerimiento 1")
    print("Se desea conocer si dos estaciones pertenecen al mismo cluster")
    station1=int(input("ID de la primera estación: "))
    station2=int(input("ID de la segunda estación: "))
    boole=controller.sameCC(cont,station1,station2)
    if boole== True:
        res=" si"
    else:
        res=" no"
    print('Las estaciones ',station1,' y ', station2,res," estan en el mismo cluster")
    print('El número de componentes fuertemente conectados es: ' +
          str(controller.numSCC(cont)))


def optionFive():
    print("Requerimiento 3")
    print("Se desea conocer el top 3 de las estaciones a las que mas bicicletas llegan provenientes de otras estaciones.\n"
            "Además, el top 3 de las estaciones de las que más viajes salen hacia otras estaciones.\n"
            "También, el top 3 de las estaciones menos utilizadas por los turistas ")
    topA=controller.top(cont['#trips_arr'])
    topD=controller.top(cont['#trips_dep'])
    noTop=controller.noTop(cont['#trips_sum'],topA[0])

    print("El top 3 de llegadas  es: ",topA[0],",",topA[1],",",topA[2])
    print("El top 3 de salidas  es: ",topD[0],",",topD[1],",",topD[2])
    print("El top 3 de las menos utilizadas es: ",noTop[0],",",noTop[1],",",noTop[2])


def optionSeven():
    print("Requerimiento 6")
    print("Se desea conocer la estación más cercana a un turista y al sitio turístico que quiere visitar.\n"
            "También, la lista de estaciones y el tiempo más corto para llegar a su destino.")
    lat1=float(input("Ingrese la latitud de su ubicación actual: "))
    lon1=float(input("Ingrese la longitud de su ubicación actual: "))
    lat2=float(input("Ingrese la latitud del sitio turístico al que quiere viajar: "))
    lon2=float(input("Ingrese la longitud del sitio turístico al que quiere viajar: "))
    nearTurist=controller.stationNear(cont['geografic_station'],lat1,lon1)
    nearTuristic=controller.stationNear(cont['geografic_station'],lat2,lon2)
    theBest=controller.theBestRoute(cont['connections'], nearTurist,nearTuristic)
    print("La estación más cercana a usted es: ",nearTurist)
    print("La estación más cercana al sitio turístico al que quiere viajar es: ", nearTuristic)
    if theBest[0] != None:
        while not(stack.isEmpty(theBest[0])):
            station=stack.pop(theBest[0])
            vertA=station['vertexA']
            vertB=station['vertexB']
            print(vertA,'->',vertB)
        print("El tiempo estimado de viaje es: ",theBest[1])
    else:
        print("No existe ruta entre ", nearTurist," y ",nearTuristic)
def optionFour():
    print("Requerimiento 2")
    print("Se desea conocer las rutas circulares que se pueden realizar en un estimado espacio de tiempo")
    time1=int(input('Escriba el tiempo minimo que estima para su visita de la ciudad: '))*60
    time2=int(input('Escriba el tiempo maximo que tiene para visitar la ciudad: '))*60
    start=int(input('Escriba el id de la estación de la que desea empezar su recorrido: '))
    result=controller.FindCycles(cont,start,time1,time2)
    
    cycles=it.newIterator(result)
    print("hay ",lt.size(result),"rutas circulares que se pueden visitar en el tiempo dado \n Estos son: \n")
    while it.hasNext(cycles):
        print("-----------------------------")
        cycle=it.next(cycles)
        
        cycleit= it.newIterator(cycle)
        while it.hasNext(cycleit):
            edge=it.next(cycleit)
            if edge!=None:
                print("salida",edge["vertexA"],"llegada",edge["vertexB"],"tiempo estimado",round(edge["weight"]/60,2),"min\n")

def optionSix():
    print("Requerimiento 5")
    print("Se desea conocer las estaciones con más entradas y salidas para un rango de edad y el camino más corto entre dos estaciones")
    
    start=int(input('Escriba el rango de edades que quiere conocer \n0=> 0-10 \n1=> 11-20 \n2=> 21-30 \n3=> 31-40 \n4=> 41-50 \n5=> 51-60\n6=> +60\n '))
    result=controller.getmincostpathage(cont,start)
    list_vert=result[0]
    salida=result[1][0]
    llegada=result[1][1]
    print("La estación de la que más salen personas de esta edad es",salida,"la estación a la que más llegan personas de esta edas es",llegada)
    print("El camino más corto entre estas estaciones es:")
    if list_vert[0] != None:
        while not(stack.isEmpty(list_vert[0])):
            station=stack.pop(list_vert[0])
            vertA=station['vertexA']
            vertB=station['vertexB']
            print(vertA,'->',vertB)
        print("El tiempo estimado de viaje es: ",round(list_vert[1]/60,2),"min")
    else:
        print("No existe ruta entre ",salida ," y ", llegada)

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

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    elif int(inputs[0])==4:
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    elif int(inputs[0])==6:
        executiontime = timeit.timeit(optionSix, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 7:
        executiontime = timeit.timeit(optionSeven, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    else:
        sys.exit(0)
sys.exit(0)
