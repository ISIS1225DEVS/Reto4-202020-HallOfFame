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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.DataStructures import edge as ed
from DISClib.DataStructures import orderedmapstructure as om
assert config
from math import radians, cos, sin, asin, sqrt 

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newAnalyzer():

    try:
        citibike = {
                    'stops': None,
                    'connections': None,
                    'components': None,
                    'paths': None,
                    '#trips_dep':None,
                    '#trips_arr':None,
                    'geografic_station':None,
                    'age':None
                    
                    }

        citibike['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=1000,
                                              comparefunction=compareStations)
        citibike['#trips_dep']=  m.newMap(numelements=1000,
                                     maptype='PROBING',
                                     comparefunction=compareTrips)
        citibike['#trips_arr']=  m.newMap(numelements=1000,
                                     maptype='PROBING',
                                     comparefunction=compareTrips)
        citibike['#trips_sum']=  m.newMap(numelements=1000,
                                     maptype='PROBING',
                                     comparefunction=compareTrips)
        citibike['geografic_station']= m.newMap(numelements=1000,
                                     maptype='PROBING',
                                     comparefunction=compareTrips)
        
        citibike['age']=m.newMap(numelements=10,
                                     maptype='PROBING',
                                     comparefunction=compareStations)
        for i in range (0,7):
            x=m.newMap(2000,maptype='CHAINING',
                                     comparefunction=compareStationsSpecial)
            m.put(citibike['age'],i,x)
        return citibike
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al grafo

def addTrip(citibike,trip):
    try:
        origin= int(trip['start station id'])
        destination= int(trip ['end station id'])
        if origin != destination:
            origin_name= str(trip['start station name'])
            destination_name= str(trip['end station name'])
            duration = int(trip ['tripduration'])
            sLatitude=float(trip['start station latitude'])
            sLongitude=float(trip['start station longitude'])
            eLatitude=float(trip['end station latitude'])
            eLongitude=float(trip['end station longitude'])
            addStation(citibike, origin)
            addStation(citibike, destination)
            addConnection (citibike, origin, destination, duration)
            addNumTrips(citibike['#trips_dep'],origin_name)
            addNumTrips(citibike['#trips_arr'],destination_name)
            addNumTrips(citibike['#trips_sum'],origin_name)
            addNumTrips(citibike['#trips_sum'],destination_name)
            addGeograficStation(citibike['geografic_station'],sLatitude,sLongitude,origin)
            addGeograficStation(citibike['geografic_station'],eLatitude,eLongitude,destination)
            updateage(citibike,trip)
        return citibike
    except Exception as exp:
        error.reraise(exp, 'model:addTrip')


def addGeograficStation(keycitibike,lat,lon, stationid):
    geo=(lat,lon)
    entry = m.get(keycitibike, stationid)
    if entry == None:
        m.put(keycitibike,stationid, geo)
    
    return keycitibike


def addNumTrips(keycitibike, nameStation):
    numtrip=0
    entry = m.get(keycitibike, nameStation)
    if entry == None:
        numtrip=1
    else:
        actnum=entry['value']
        if actnum==0:
            numtrip=1
        else:
            numtrip=actnum + 1
    m.put(keycitibike,nameStation,numtrip)
    return keycitibike


def addStation(citibike, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(citibike['connections'], stationid):
            gr.insertVertex(citibike['connections'], stationid)
        return citibike
    except Exception as exp:
        error.reraise(exp, 'model:addStation')
 

def addConnection(citibike, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(citibike['connections'], origin, destination)
    if edge is None:
        gr.addEdge(citibike['connections'], origin, destination, duration)
    else:
        ed.averageWeight(edge,duration)
    return citibike



# ==============================
# Funciones de consulta
# ==============================

def numSCC(citibike):
    sc=scc.KosarajuSCC(citibike['connections'])
    return scc.connectedComponents(sc)

def sameCC(citibike,station1, station2):
    sc=scc.KosarajuSCC(citibike['connections'])
    return scc.stronglyConnected(sc,station1,station2)

def theTop(mapa):
    res=[]
    while len(res) < 3:
        topv=0
        keys= m.keySet(mapa)
        values=m.valueSet(mapa)
        itv=it.newIterator(values)
        itk=it.newIterator(keys)
        while it.hasNext(itv):
            value=it.next(itv)
            key= it.next(itk)
            if value>topv:
                topv=value
                topk=key
        res.append(topk)
        m.remove(mapa,topk)
    return res 

def theNoTop(mapa,mayor):
    res=[]
    while len(res) < 3:
        couple=m.get(mapa,mayor)
        ntopv=couple['value']
        keys= m.keySet(mapa)
        values=m.valueSet(mapa)
        itv=it.newIterator(values)
        itk=it.newIterator(keys)
        while it.hasNext(itv):
            value=it.next(itv)
            key= it.next(itk)
            if value<ntopv:
                ntopv=value
                ntopk=key
        res.append(ntopk)
        m.remove(mapa,ntopk)

    return res  
        

def distance(lat1, lat2, lon1, lon2): 
    # radians which converts from degrees to radians. 
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
       
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  
    c = 2 * asin(sqrt(a))  
     
    # Radius of earth in kilometers. Use 3956 for miles 
    r = 6371
       
    # calculate the result 
    return(c * r) 


def stationNear(mapa,lat1,lon1):
    keys= m.keySet(mapa)
    values=m.valueSet(mapa)
    small=m.get(mapa,72)
    valorilt=small['value'][0]
    valorilo=small['value'][1]
    Thedis=distance(valorilt,lat1,valorilo,lon1)
    itv=it.newIterator(values)
    itk=it.newIterator(keys)
    while it.hasNext(itv):
        value=it.next(itv)
        key= it.next(itk)
        lat= value[0]
        lon=value[1]
        dist=distance(lat1,lat,lon1,lon)
        if dist<Thedis:
            Thedis=dist
            station=key

    return station


def theBestRoute(graph,station1,station2):
    best=djk.Dijkstra(graph,station1)
    wa=djk.pathTo(best,station2)
    y=djk.distTo(best,station2)
    if wa==None:
        way="No existe ruta "
    way=[wa,y]
    return way 

def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    return scc.connectedComponents(analyzer['components'])


def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['connections'], initialStation)
    return analyzer


def hasPath(analyzer, destStation):
    """
    Indica si existe un camino desde la estacion inicial a la estación destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    return djk.hasPathTo(analyzer['paths'], destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])


def servedRoutes(analyzer):
    """
    Retorna la estación que sirve a mas rutas.
    Si existen varias rutas con el mismo numero se
    retorna una de ellas
    """
    lstvert = m.keySet(analyzer['stops'])
    itlstvert = it.newIterator(lstvert)
    maxvert = None
    maxdeg = 0
    while(it.hasNext(itlstvert)):
        vert = it.next(itlstvert)
        lstroutes = m.get(analyzer['stops'], vert)['value']
        degree = lt.size(lstroutes)
        if(degree > maxdeg):
            maxvert = vert
            maxdeg = degree
    return maxvert, maxdeg


def circularroutes(analyzer,startvertex,time1,time2):
    sc=scc.KosarajuSCC(analyzer['connections'])
    dfsdata=dfscircular(analyzer['connections'],startvertex,sc)['cycles']
    
    dfsdatait=it.newIterator(dfsdata)
    respuesta=lt.newList()
    while it.hasNext(dfsdatait):
        x=it.next(dfsdatait)
        camino=filtrodetiempo(x,time1,time2,analyzer['connections'])
        if not camino == None:
            lt.addLast(respuesta,camino)
    return respuesta


def updateage(analyzer,trip):
    age_analyzer=analyzer['age']
    birth=int(trip['birth year'])
    age= 2018-birth
    agerange=(age-1)//10
    if agerange>6:
        agerange=6
    
    age_dict=me.getValue(m.get(age_analyzer,agerange))

    InS=int(trip['end station id'])

    InS_c=m.get(age_dict,InS)
    
    if InS_c==None:
        m.put(age_dict,InS,[1,0])
        InSprev=[1,0]
    else:
        InSprev=me.getValue(InS_c)
        InSprev[0]=InSprev[0]+1
        m.put(age_dict,InS,InSprev)


    OutS=int(trip['start station id'])
    OutS_c=m.get(age_dict,OutS)

    if OutS_c==None:
        m.put(age_dict,OutS,[0,1])
        OutSprev=[1,0]
    else:
        OutSprev=me.getValue(OutS_c)
        OutSprev[1]=OutSprev[1]+1
        m.put(age_dict,OutS,OutSprev)
    

    MaxO_c=m.get(age_dict,'MaxO')
    MaxI_c=m.get(age_dict,'MaxI')
    
    if MaxI_c==None:
        MaxI=InS
        m.put(age_dict,'MaxI',InS)
    else:
        MaxI=me.getValue(MaxI_c)
        if me.getValue(m.get(age_dict,MaxI))[0]<InSprev[0]:
            m.put(age_dict,'MaxI',InS)

    if MaxO_c==None:
        MaxO=OutS
        m.put(age_dict,'MaxO',OutS)
    else:
        MaxO=me.getValue(MaxI_c)
        if me.getValue(m.get(age_dict,MaxO))[1]<OutSprev[1]:
            m.put(age_dict,'MaxO',OutS)

def getmincostpathage(analyzer,age):
    a=getmaxage(analyzer,age)
    z=theBestRoute(analyzer['connections'],a[0],a[1])

    return z,a
def theBestRoute(graph,station1,station2):
    best=djk.Dijkstra(graph,station1)
    wa=djk.pathTo(best,station2)
    y=djk.distTo(best,station2)
    if wa==None:
        way="No existe ruta "
    way=[wa,y]
    return way
# ==============================
# Funciones Helper
# ==============================
def getmaxage(analyzer,age):
    age_analyzer=analyzer['age']
    
    age_dict=me.getValue(m.get(age_analyzer,age))

    MaxO=me.getValue(m.get(age_dict,'MaxO'))
    MaxI=me.getValue(m.get(age_dict,'MaxI'))
    return MaxO,MaxI

def cleanServiceDistance(lastservice, service):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if service['Distance'] == '':
        service['Distance'] = 0
    if lastservice['Distance'] == '':
        lastservice['Distance'] = 0


def formatVertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['BusStopCode'] + '-'
    name = name + service['ServiceNo']
    return name

def dfscircular(graph,source,sc):
    try:
        search = {
                  'source': source,
                  'visited': None,
                  'cycles':None
                  }

        search['visited'] = m.newMap(numelements=gr.numVertices(graph),
                                       maptype='PROBING',
                                       comparefunction=graph['comparefunction']
                                       )
        search['cycles'] =lt.newList()
        m.put(search['visited'], source, {'marked': True, 'edgeTo': None})
        dfsVertexc(search, graph, source, source ,sc)
        return search
    except Exception as exp:
        error.reraise(exp, 'dfs:DFS')

def dfsVertexc(search,graph,vertex,source,sc):
    try:
        adjlst = gr.adjacents(graph, vertex)
        
        adjslstiter = it.newIterator(adjlst)
        while (it.hasNext(adjslstiter)):
            w = it.next(adjslstiter)
            visited = m.get(search['visited'], w)
            
                
            if visited is None:
                m.put(search['visited'],w, {'marked': True, 'edgeTo': vertex})
                if scc.stronglyConnected(sc,w,source):
                    dfsVertexc(search, graph, w, source, sc)
            elif w == source and gr.getEdge(graph,vertex,source)!=None:
                cycle=lt.newList()
                lt.addLast(cycle,vertex)
                lt.addLast(cycle,w)
                x=me.getValue(m.get(search['visited'],vertex))['edgeTo']
                
                while x != None:
                    lt.addFirst(cycle,x)
                    x=me.getValue(m.get(search['visited'],x))['edgeTo']
                lt.addLast(search['cycles'],cycle)
        return search
    except Exception as exp:
        error.reraise(exp, 'dfs:dfsVertex')

def filtrodetiempo(cycle,time1, time2,graph):
    lstit=it.newIterator(cycle)
    cycleinfo=lt.newList()
    last=None
    time=0
    while it.hasNext(lstit) :
        actual=it.next(lstit)
        time+=20
        if last!=None and actual!=None:
            edge=gr.getEdge(graph,last,actual)
            
            if edge !=None:
                time+=edge['weight']
            lt.addLast(cycleinfo,edge)
        last=actual
    if time>time1 and time<time2:
        return cycleinfo
    else :
        return None



# ==============================
# Funciones de Comparacion
# ==============================

def compareStations(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1
def compareStationsSpecial(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    else:
        return -1


def compareTrips(trip1, route2):
    """
    Compara dos rutas
    """
    trip2=route2['key']
    if (trip1 == trip2):
        return 0
    elif (trip1 > trip2):
        return 1
    else:
        return -1
