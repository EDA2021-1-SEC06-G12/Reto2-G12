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

    videosfile = cf.data_dir + 'videos-large.csv'
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


def req2(catalog,country):
    x=model.dias(catalog,country,'countries')
    return 'title: '+x[0]+' || channel_title: '+x[1]+' || country: '+str(x[2])+' || días: '+str(x[4])

def req3(catalog,categoria):
    ide=model.idporcategory(categoria,catalog)
    x=model.dias(catalog,ide,'ids')
    return 'title: '+x[0]+' || channel_title: '+x[1]+' || category_id: '+str(x[3])+' || días: '+str(x[4])

def req4(catalog,pais,tag,n):
    lista=model.tags(catalog,pais,tag)
    ordered=model.sortVideos(lista,lt.size(lista),model.cmpVideosbyLikes)[1]
    final=model.sacar(n,ordered)
    cadena=''
    i=it.newIterator(final)
    n=0
    while it.hasNext(i):
        n+=1
        v=it.next(i)
        cadena=cadena+'\nPuesto '+str(n)+'\ntitle: '+v['title']+' || channel_title: '+v['channel_title']+' || publish_time: '+str(v['publish_time'])+' || views: '+str(v['views'])+' || likes: '+str(v['likes'])+' || dislikes: '+str(v['dislikes'])+'\ntags: '+v['tags']+'\n'
    return cadena

#########

def R1(categoria,pais,num,catalog): 
    ID=model.ID_dado_category_name(categoria,catalog)
    if ID==None:
        return 'Categoría no válida'
    else:
        mapa = catalog["map_categories_country"]
        key = pais+categoria
        entrada = mp.get(mapa,key)
        valor = entrada["value"]
        l = valor["videos"]
        if l==None:
            return 'País no válido.'
        else:
            l2=model.sortVideos(l,lt.size(l),model.cmpVideosbyViews)[1]
            if num>lt.size(l2):
                return 'El número ingresado excede la cantidad de videos que cumplen con los requisitos. Intente con un número igual o menor a '+str(lt.size(l))
            else:
                n=0
                c=''
                final=lt.subList(l2,1,num)
                i=it.newIterator(final)
                while it.hasNext(i):
                    n+=1
                    vid=it.next(i)
                    c=c+'\nPuesto '+str(n)+'\ntrending_date: '+str(vid['trending_date'])+'; title: '+vid['title']+'; channel_title: '+vid['channel_title']+'; publish_time: '+vid['publish_time']+'; views: '+vid['views']+'; likes: '+vid['likes']+ '; dislikes: '+vid['dislikes']+'\n'
                return 'Información de los '+str(num)+' videos con más views en '+pais+' para la categoría de '+categoria+':\n'+c 


def R2(pais,catalog):
    entry = mp.get(catalog["map_countries"],pais)
    entry = entry["value"]
    l1 = entry["videos"]
    print(lt.size(l1))
    tabla = model.tabla_mas_trending(l1)
    mas_trending = model.mas_trending(tabla)
    info = lt.getElement(mas_trending[2],1)
    return '\nInformación del video trending por más días en '+pais+':\ntitle: '+lt.getElement(info,2)+'; channel_title: '+lt.getElement(info,3)+'; country: '+ pais+'; días: '+str(mas_trending[1])


def R3(categoria,rep,catalog):
    ID=model.ID_dado_category_name(categoria,catalog)
    if ID==None:
        return 'Categoría no válida'
    else:
        l1=model.lporcategoria(ID,catalog['videos'])
        l2=model.sortVideos(l1,lt.size(l1),model.cmpVideosbyTitleandDate)[1]
        if rep==1:
            tupla=model.maxnorep('title',l2)
        elif rep==0:
            tupla=model.maxrep('title',l2)
        else:
            return 'La opción ingresada (diferente a 0 y 1) no es válida'

        return '\nInformación del video trending por más días para la categoría de '+categoria+':\ntitle: '+tupla[0]+'; channel_title: '+tupla[1]+'; category_id: '+tupla[2]+'; días: '+str(tupla[4])
    

def R4(tag,pais,num,catalog):
    l1=model.lportyp(tag,pais,catalog['videos'])
    if l1==None:
        return 'No hay información para el país y/o tag ingresados.'
    else:
        orde=model.sortVideos(l1,lt.size(l1),model.cmpVideosbyLikes)[1]
        final=model.sacar(num,orde)
        if final==None:
            return 'El número ingresado excede la cantidad de videos que cumplen con los requisitos.'
        else:
            c=''
            i=it.newIterator(final)
            n=0
            while it.hasNext(i):
                n+=1
                v=it.next(i)
                c=c+'\nPuesto '+str(n)+'\ntitle: '+v['title']+'; channel_title: '+v['channel_title']+'; publish_time: '+str(v['publish_time'])+'; views: '+str(v['views'])+'; likes: '+str(v['likes'])+'; dislikes: '+str(v['dislikes'])+'; tags: '+v['tags']+'\n'
            return 'Información de los '+str(num)+' videos con más views en '+pais+' con el tag de '+tag+':\n'+c




    
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
