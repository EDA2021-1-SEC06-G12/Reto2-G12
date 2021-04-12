"""
 * Copyright 2020, Departamento de sistemas y Computación,
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
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv
import time
import tracemalloc

from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from datetime import datetime
from DISClib.Algorithms.Sorting import shellsort as shes
from DISClib.Algorithms.Sorting import mergesort as mrge
from DISClib.Algorithms.Sorting import quicksort as quck
from DISClib.Algorithms.Sorting import insertionsort as inss
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    return model.initCatalog()

def loadData(catalog):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    categoriesfile = cf.data_dir + "category-id.csv"
    i_file = csv.DictReader(open(categoriesfile, encoding='utf-8'), delimiter='\t')
    for category in i_file:
        model.addCategory(catalog,category)

    videosfile = cf.data_dir + 'videos-small.csv'
    input_file = csv.DictReader(open(videosfile, encoding='utf-8'))
    for video in input_file:
        video["trending_date"] = datetime.strptime(video["trending_date"],"%y.%d.%m").date()
        model.addVideo(catalog, video)
    
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)


    return delta_time, delta_memory


def req1(catalog,country,category,n):
    lista=model.getvidsby(catalog,'countries',country)
    ide=model.idporcategory(category,catalog)
    if lista==None or ide==None:
        print('\nNO HAY INFORMACIÓN PARA ESTE PAÍS O CATEGORÍA\n')
    else:
        mapa=model.countryid(lista,ide)
        i=1
        print('\nINFORMACIÓN DE LOS '+str(n)+' VIDEOS CON MÁS VIEWS EN '+country.upper()+' PARA LA CATEGORÍA '+category.upper())
        while i<=n:
            x=model.dlv(catalog,mapa,'views')
            info=x[1]
            print ('\nPUESTO '+str(i)+'\ntrending_date: '+str(info['trending_date'])+' || title: '+info['title']+' || channel_title: '+info['channel_title']+' || publish_time: '+info['publish_time']+' || views: '+info['views']+'|| likes: '+str(x[2])+' || dislikes: '+info['dislikes'])
            mp.remove(mapa,x[0])
            i+=1
        print('\n')

def req2(catalog,country):
    lista = model.getvidsby(catalog,'countries',country)
    if lista == None:
        return 'NO HAY INFORMACIÓN PARA ESTE PAÍS'
    else:
        mapa=model.titleporidc('dias',lista)
        x=model.dlv(catalog,mapa,'dias')
        info=x[1]
        return 'INFORMACIÓN DEL VIDEO TENDENCIA POR MÁS DÍAS EN '+country.upper()+'\ntitle: '+info['title']+' || channel_title: '+info['channel_title']+' || country: '+info['country']+' || días: '+str(x[2])

def req3(catalog,category):
    ide=model.idporcategory(category,catalog)
    if ide==None:
        return 'NO HAY INFORMACIÓN PARA ESTA CATEGORÍA'
    else:
        lista = model.getvidsby(catalog,'ids',ide)
        mapa=model.titleporidc('dias',lista)
        x=model.dlv(catalog,mapa,'dias')
        info=x[1]
        return 'INFORMACIÓN DEL VIDEO TENDENCIA POR MÁS DÍAS PARA LA CATEGORÍA '+category.upper()+'\ntitle: '+info['title']+' || channel_title: '+info['channel_title']+' || category_id: '+str(info['category_id'])+' || días: '+str(x[2])

def req4(catalog,country,tag,n):
    lista=model.getvidsby(catalog,'countries',country)
    if lista==None:
        print('\nNO HAY INFORMACIÓN PARA ESTE PAÍS\n')
    else:
        lista2=model.tags(catalog,lista,tag)
        if lt.size(lista2)==0:
            print('\nNO HAY INFORMACIÓN PARA ESTE TAG\n')
        else:
            mapa=model.titleporidc('likes',lista2)
            i=1
            print('\nINFORMACIÓN DE LOS '+str(n)+' VIDEOS CON MÁS LIKES EN '+country.upper()+' CON EL TAG '+tag.upper())
            while i<=n:
                x=model.dlv(catalog,mapa,'likes')
                info=x[1]
                print('\nPUESTO '+str(i)+'\ntitle: '+info['title']+' || channel_title: '+info['channel_title']+' || publish_time: '+info['publish_time']+' || views: '+info['views']+' || likes: '+str(x[2])+' || dislikes: '+info['dislikes']+'\ntags: '+info['tags'])
                mp.remove(mapa,x[0])
                i+=1
            print('\n')

#########


    
# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo


# ======================================
# Funciones para medir tiempo y memoria
# ======================================


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
