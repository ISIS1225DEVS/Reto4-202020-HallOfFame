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
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
from DISClib.DataStructures import listiterator as it
from math import radians, cos, sin, asin, sqrt
import datetime
from datetime import date
import calendar
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""
def newAnalyzer():
    analyzer = { 'accidents': None,
                'date' : None,
                'hour': None
                }
    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareIds)

    analyzer['date'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    analyzer['hour'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareHours)
    return analyzer
# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------


# Funciones para agregar informacion al catalogo
def addAccident(analyzer,accident):
    dia = accident['Start_Time']
    accidentDate = datetime.datetime.strptime(dia, '%Y-%m-%d %H:%M:%S')
    accidentYear = str(accidentDate.year)
    lt.addLast(analyzer['accidents'],accident)
    uptadeAccidentInDate(analyzer['date'], accident) 
    uptadeAccidentInHour(analyzer['hour'], accident)
    return analyzer

def uptadeAccidentInHour(map,accident):
    date = accident['Start_Time']
    accidentDate = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    formato=":"
    if accidentDate.minute>=30:
        formato=str(accidentDate.hour)+":30"
    elif accidentDate.minute<30:
        formato=str(accidentDate.hour)+":00"
   
    entry = om.get(map, formato)

    if entry is None:
        hour_entry = newHourEntry()
        om.put(map ,formato, hour_entry)  
    else:
        hour_entry = me.getValue(entry)
    
    lt.addLast(hour_entry['accidents'], accident)
    addSeverityToDate(hour_entry['severities'],accident)
    addStateToDate(hour_entry['state'],accident)
    return map

def uptadeAccidentInDate(map,accident):
    date = accident['Start_Time']
    accidentDate = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentDate.date())

    if entry is None:
        date_entry = newDateEntry()
        om.put(map ,accidentDate.date(), date_entry)  
    else:
        date_entry = me.getValue(entry)
    
    lt.addLast(date_entry['accidents'], accident)
    addSeverityToDate(date_entry['severities'],accident)
    addStateToDate(date_entry['state'],accident)
    return map

def addSeverityToDate(dateEntry,accident):
    
    severity = accident['Severity']
    entry = m.get(dateEntry, severity)

    if entry is None:
        severity_entry = newSeverityEntry(accident)
        m.put(dateEntry , severity, severity_entry)
    else:
        severity_entry = me.getValue(entry)
        
    lt.addLast(severity_entry['listBySeverity'],accident)
    return dateEntry

def addStateToDate(dateEntry,accident):
    
    state = accident['State']
    entry = m.get(dateEntry, state)

    if entry is None:
        state_entry = newState(accident)
        m.put(dateEntry , state, state_entry)
    else:
        state_entry = me.getValue(entry)
        
    lt.addLast(state_entry['listByState'],accident)
    return dateEntry

def newHourEntry():
 
    entry = {'severities': None, 'accidents': None, 'state':None}
    entry['severities'] = m.newMap(numelements=15, maptype='PROBING', comparefunction=compareSeverities)
    entry['state'] = m.newMap(numelements=15, maptype='PROBING',comparefunction=comparestates)
    entry['accidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newDateEntry():
 
    entry = {'severities': None, 'accidents': None, 'state':None}
    entry['severities'] = m.newMap(numelements=15,
                                     maptype='PROBING',
                                     comparefunction=compareSeverities)
   
    entry['state'] = m.newMap(numelements=15, maptype='PROBING',comparefunction=comparestates)

    entry['accidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newState(accident):
  
    state_entry = {'state': None, 'listByState': None}
    state_entry['state'] = accident['State']
    state_entry['listByState'] = lt.newList('SINGLE_LINKED', comparestatesl)
    return state_entry

def newSeverityEntry(accident):
  
    severity_entry = {'severity': None, 'listBySeverity': None}
    severity_entry['severity'] = accident['Severity']
    severity_entry['listBySeverity'] = lt.newList('SINGLE_LINKED', compareSeveritiesl)
    return severity_entry
# ==============================
# Funciones de consulta
# ==============================

def accisSize(analyzer):
    return lt.size(analyzer['accidents'])

def indexHeight(analyzer):
    return om.height(analyzer['date'])

def indexSize(analyzer):
    return om.size(analyzer['date'])

def minKey(analyzer):
    return om.minKey(analyzer['date'])

def maxKey(analyzer):
    return om.maxKey(analyzer['date'])

def getAccidentsByDate(analyzer, day):
    """
    Para una fecha determinada, retorna el numero de accidentes
    por severidad.
    """
    aDate = om.get(analyzer['date'], day)
    if aDate['key'] is not None:
        Accismap = me.getValue(aDate)['severities']
        sev=m.keySet(Accismap)
        iterator= it.newIterator(sev)
        totales=0
        while(it.hasNext(iterator)):
            severity1= it.next(iterator)
            numaccis = m.get(Accismap,severity1)
            lista= numaccis['value']
            cuantas = lt.size(lista['listBySeverity'])
            totales+=cuantas
            if lista is not None:
                print("severidad: "+ str(severity1) + " tiene : " +str(cuantas) +" accidentes")
        print("accidentes totales: "+str(totales))

def getAccidentsLast(analyzer, day):
    
    aDate = om.keys(analyzer['date'],om.minKey(analyzer['date']),day)
    iterator= it.newIterator(aDate)
    cuantos=0
    diaMayor=None
    cuantosMayor=0
    while (it.hasNext(iterator)):
        info= it.next(iterator)
        valor = om.get(analyzer['date'],info)['value']
        cuantos += lt.size(valor['accidents'])
        if(lt.size(valor['accidents'])>cuantosMayor):
            cuantosMayor=lt.size(valor['accidents'])
            diaMayor=info
    print("accidentes totales: "+str(cuantos)+", la fecha con mayor accidentes es : "+str(diaMayor))

def getAccidentsState(analyzer, dayin, dayend):
    
    aDate = om.keys(analyzer['date'],dayin,dayend)
    iterator= it.newIterator(aDate)
    cuantos=0
    diaMayor=None
    cuantosMayor=0
    while (it.hasNext(iterator)):
        info= it.next(iterator)
        valor = om.get(analyzer['date'],info)['value']
        cuantos += lt.size(valor['accidents'])
        llaves = m.keySet(valor['state'])
        iterator1= it.newIterator(llaves)
        while(it.hasNext(iterator1)):
            info1= it.next(iterator1)
            val = m.get(valor['state'], info1)['value']['listByState']
            if(lt.size(val)>cuantosMayor):
                cuantosMayor=lt.size(val)
                diaMayor=info1
    print("accidentes totales: "+str(cuantos)+", el estado con mayor accidentes es : "+str(diaMayor)+" con : " +str(cuantosMayor))

def getAccidentsHour(analyzer, dayin, dayend):
    
    aDate = om.keys(analyzer['hour'],dayin,dayend)
    iterator= it.newIterator(aDate)
    sev = m.newMap(numelements=15, maptype='PROBING', comparefunction=compareSeverities)
    cuantos=0
    while (it.hasNext(iterator)):
        info= it.next(iterator)
        valor = om.get(analyzer['hour'],info)['value']
        cuantos += lt.size(valor['accidents'])
        llaves = m.keySet(valor['severities'])
        iterator1= it.newIterator(llaves)
        while(it.hasNext(iterator1)):
            info1= it.next(iterator1)
            val = m.get(valor['severities'], info1)['value']['listBySeverity']
            entry = m.get(sev, info1)
            if(entry is None):
                dic={'severity': info1, 'cuantos':lt.size(val)}
                m.put(sev,info1,dic)
            else:
                entry['value']['cuantos']+=lt.size(val)
    
    data=" "
    cuan=0
    keys= m.keySet(sev)
    ite=it.newIterator(keys)
    while(it.hasNext(ite)):
        inf=it.next(ite)
        value = m.get(sev,inf)['value']['cuantos']
        if(value>cuan):
            cuan= value
            data= inf

            
    print("accidentes totales: "+str(cuantos)+", la severidad con mayor \n accidentes es : "+str(data)+ "con : "+str(cuan)+" accidentes.")

def getAccidentsCategory(analyzer, hourin, hourend):

    
    aDate = om.keys(analyzer['date'],hourin,hourend)
    iterator= it.newIterator(aDate)
    cuantos=0
    diaMayor=None
    cuantosMayor=0
    
    while (it.hasNext(iterator)):
        info= it.next(iterator)
        valor = om.get(analyzer['date'],info)['value']
        cuantos += lt.size(valor['accidents'])
        llaves = m.keySet(valor['severities'])
        iterator1= it.newIterator(llaves)
        while(it.hasNext(iterator1)):
            info1= it.next(iterator1)
            val = m.get(valor['severities'], info1)['value']['listBySeverity']
            if(lt.size(val)>cuantosMayor):
                cuantosMayor=lt.size(val)
                diaMayor=info1
    print("accidentes totales: "+str(cuantos)+", la severidad con mayor accidentes es : "+str(diaMayor))

def getRadius(analyzer, lat1, lon1, rad):
    """
    sacarle accidente por acc 
    """
    lista=lt.newList()
    actualizar(lista)
    iterador= it.newIterator(analyzer['accidents'])
    radius = rad # in miles
    cuantos=0
    while(it.hasNext(iterador)):
        info = it.next(iterador)
        lat2 = info['Start_Lat']
        lon2 = info['Start_Lng']
        date = info['Start_Time']
        accidentDate = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        a = haversine(lon1, lat1, float(lon2), float(lat2))
        if a <= radius:
            cuantos += 1 
            dia= accidentDate.date().weekday()
            camb = lt.getElement(lista, dia)
            camb['veces']+=1
    veces=0
    mayor=''
    for i in range(7):
        el=lt.getElement(lista, i)
        if(el['veces']> veces):
            veces = el['veces']
            mayor = el['dia']

    print("los accidentes en ese radio fueron : "+ str(cuantos)+" , el dia de la semana con mayor \n accidentes en ese radio es: "+ str(mayor)+", con: "+ str(veces))

def actualizar(lista):
    formato0 = {'llave':0, 'dia':"domingo", 'veces':0}
    formato1 = {'llave':1, 'dia':"lunes", 'veces':0}
    formato2 = {'llave':2, 'dia':"martes", 'veces':0}
    formato3 = {'llave':3, 'dia':"miercoles", 'veces':0}
    formato4 = {'llave':4, 'dia':"jueves", 'veces':0}
    formato5 = {'llave':5, 'dia':"viernes", 'veces':0}
    formato6 = {'llave':6, 'dia':"sabado", 'veces':0}
    for i in range (7):
        if(i==0):
            lt.addLast(lista, formato0)
        elif(i==1):
            lt.addLast(lista, formato1)
        elif(i==2):
            lt.addLast(lista, formato2)
        elif(i==3):
            lt.addLast(lista, formato3)
        elif(i==4):
            lt.addLast(lista, formato4)
        elif(i==5):
            lt.addLast(lista, formato5)
        elif(i==6):
            lt.addLast(lista, formato6)

    print(lt.getElement(lista,0))  
    print(lt.getElement(lista,5))  
    print(lt.getElement(lista,3))  
# ==============================
# Funciones de Comparacion
# ==============================

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    formula tomada de https://stackoverflow.com/questions/42686300/how-to-check-if-coordinate-inside-certain-area-python
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 # Radius of earth in miles. Use 3956 for miles
    return c * r


def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareDates(date1, date2):

    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else: 
        return -1

def compareSeverities(Sev1, Sev2):
    if (Sev1 == Sev2['key']):
        return 0
    elif (Sev1 > Sev2['key']) :
        return 1
    else:
        return -1

def compareSeveritiesl(cat1, cat2):
    if (cat1 == cat2):
        return 0
    elif (cat1 > cat2):
        return 1
    else:
        return -1

def comparestates(state1, state2):
    if (state1 == state2['key']):
        return 0
    elif (state1 > state2['key']) :
        return 1
    else:
        return -1

def comparestatesl(state1, state2):
    if (state1 == state2):
        return 0
    elif (state1 > state2) :
        return 1
    else:
        return -1

def compareHours(hour1, hour2):
    if (hour1 == hour2):
        return 0
    elif (hour1 > hour2) :
        return 1
    else:
        return -1
