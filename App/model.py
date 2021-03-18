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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import time
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.Algorithms.Sorting import shellsort as shes
from DISClib.Algorithms.Sorting import insertionsort as inss
from DISClib.Algorithms.Sorting import selectionsort as sels
from DISClib.Algorithms.Sorting import mergesort as mrge
from DISClib.Algorithms.Sorting import quicksort as quck
from DISClib.DataStructures import listiterator as it
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def initCatalog():
    catalog= {'videos': None,
            'categories': None}
    
    catalog['videos']=lt.newList(datastructure='ARRAY_LIST', cmpfunction=cmpInit)
    catalog['categories'] = mp.newMap(35,
                                   maptype='PROBING',
                                   loadfactor=0.8,
                                   comparefunction=None)

def addVideo(catalog,video):
    lt.addLast(catalog['videos'],video)

def addCategory(catalog,category):
    lt.addLast(catalog['categories'],category)

# Funciones de consulta

def categoriaporID(name,catalog):
    """Recibe el nombre de una categoría y halla su respectivo ID
        name(str): nombre de la categoría
        catalog: catalog
    retorna:
        str: ID de la categoría"""

    categorias=catalog['categories']
    i=1
    while i<=lt.size(categorias):
        c=lt.getElement(categorias,i)
        if name.lower() in (c['name']).lower():
            return c['id']
        i+=1


def lporcyp(ID,pais,lista):
    """Crea una lista de videos de la categoría y el país requeridos
        ID(int): ID de la categoría de los videos a seleccionar
        pais(str): país de los videos a seleccionar
        lista: lista general
    retorna:
        lista: con sólo los elementos que cumplen con los parámetros"""
    v=it.newIterator(lista)
    final=lt.newList(datastructure='ARRAY_LIST')
    while it.hasNext(v):
        x=it.next(v)
        if x['country']==pais and x['category_id']==ID:
            lt.addLast(final,x)
    if lt.isEmpty(final)==True:
        return None
    else:
        return final


def lporcategoria(ID,lista):
    """Crea una lista de videos de la categoría requerida
        ID(int): ID de la categoría de los videos a seleccionar
        lista: lista general
    retorna:
        lista: con sólo los elementos que cumplen con los parámetros"""
    final=lt.newList(datastructure='ARRAY_LIST')
    i=it.newIterator(lista)
    while it.hasNext(i):
        v=it.next(i)
        if v['category_id']==ID:
            lt.addFirst(final,v)
    if lt.isEmpty(final)==True:
        return None
    else:
        return final


def lporpais(pais,lista):
    """Crea una lista de videos del país requerido
        pais(str): país de los videos a seleccionar
        lista: lista general
    retorna:
        lista: con sólo los elementos que cumplen con los parámetros"""
    final=lt.newList(datastructure='ARRAY_LIST')
    i=it.newIterator(lista)
    while it.hasNext(i):
        v=it.next(i)
        if pais.lower() == v['country'].lower():
            lt.addLast(final,v)
    if lt.size(final)==0:
        return None
    else:
        return final


def lportyp(tag,pais,lista):
    """Crea una lista de videos del tag y el país requeridos
        tag: tag presente en los videos a seleccionar
        pais(str): país de los videos a seleccionar
        lista: lista general
    retorna:
        lista: con sólo los elementos que cumplen con los parámetros"""
    i=it.newIterator(lista)
    final=lt.newList(datastructure='ARRAY_LIST')
    while it.hasNext(i):
        x=it.next(i)
        if tag in x['tags'] and pais.lower()==x['country']:
            lt.addLast(final,x)
    if lt.isEmpty(final)==True:
        return None
    else:
        return final


def maxnorep(parametro,lista):
    """Halla el video con más días siendo tendencia considerando que la misma fecha para dos países diferentes son lo mismo
        parametro: con el cual compara los videos para revisar si son el mismo
        lista: lista de videos
    retorna:
        tupla: con distintas variables del video"""
    title=''
    mayortotal=0
    mayorparcial=1
    n=2
    while n<=lt.size(lista):
        vid=lt.getElement(lista,n)
        ant=lt.getElement(lista,n-1)
        l=lt.newList()
        lt.addLast(l,ant['trending_date'])
        if vid[parametro]==ant[parametro]:
            if lt.isPresent(l,vid['trending_date'])==0:
                lt.addLast(l,vid['trending_date'])
                mayorparcial+=1
        else:
            l=lt.newList()
            lt.addLast(l,vid['trending_date'])
            if mayorparcial>mayortotal:
                mayortotal=mayorparcial
                title=ant['title']
                channel_title=ant['channel_title']
                category_id=ant['category_id']
                country=ant['country']

            mayorparcial=1
        n+=1

    if mayorparcial>mayortotal:
        mayortotal=mayorparcial
        title=ant['title']
        channel_title=ant['channel_title']
        category_id=ant['category_id']
        country=ant['country']

    return title,channel_title,category_id,country,mayortotal


def maxrep(parametro,lista):
    """Halla el video con más días siendo tendencia sin considerar que la misma fecha para dos países diferentes son lo mismo
        parametro: con el cual compara los videos para revisar si son el mismo
        lista: lista de videos
    retorna:
        tupla: con distintas variables del video"""
    mayorparcial=1
    mayortotal=1
    title=''
    i=2
    while i<=lt.size(lista):
        v=lt.getElement(lista,i)
        ant=lt.getElement(lista,i-1)
        if v[parametro]==ant[parametro]:
            mayorparcial+=1
        else:
            if mayorparcial>mayortotal:
                mayortotal=mayorparcial
                title=ant['title']
                channel_title=ant['channel_title']
                category_id=ant['category_id']
                country=ant['country']
            mayorparcial=1
        i+=1

    if mayorparcial>mayortotal:
        mayortotal=mayorparcial
        title=ant['title']
        channel_title=ant['channel_title']
        category_id=ant['category_id']
        country=ant['country']

    return title,channel_title,category_id,country,mayortotal


def sacar(num,lista):
    """No permite que se repita un video en una lista
        num: número de elementos de la nueva lista
        lista: lista general
    retorna:
        lista sin valores repetidos."""
    if num<=lt.size(lista):
        titulos=lt.newList(datastructure="ARRAY_LIST")
        final=lt.newList(datastructure="ARRAY_LIST")
        primero=lt.firstElement(lista)
        lt.addLast(titulos,primero['title'])
        lt.addLast(final,primero)
        i=it.newIterator(lista)
        while it.hasNext(i) and lt.size(final)<num:
            v=it.next(i)
            tit = v["title"]
            x = lt.isPresent(titulos,tit)
            if x == 0:
                lt.addLast(titulos,v['title'])
                lt.addLast(final,v)
        return final
    else:
        return None



# Funciones para creacion de datos


    

# Funciones utilizadas para comparar elementos dentro de una lista
def cmpInit(video1,video2):
    if int(video1["views"])==int(video2["views"]):
        return 0
    elif int(video1["views"])>int(video2["views"]):
        return 1
    else:
        return -1
    
def cmpVideosbyViews(video1,video2):
    return(int(video1["views"])>=int(video2["views"]))

def cmpVideosbyLikes(video1,video2):
    return(int(video1["likes"])>=int(video2["likes"]))

def cmpVideosbyTitleandDate(video1,video2):
    if (video1['title'])>(video2['title']):
        return True
    elif video1['title']==video2['title']:
        return video1['trending_date']>video2['trending_date']

def cmpVideosbyTitle(video1,video2):
    return (video1['title'])>=(video2['title'])

def cmpVideosbyTitleandLikes(video1,video2):
    if (video1['title'])>(video2['title']):
        return True
    elif video1['title']==video2['title']:
        return video1['likes']>video2['likes']


# Funciones de ordenamiento

def sortVideos(lista,size,cmpfunction):
    if size <= lt.size(lista):
        sub_list = lt.subList(lista, 1, size)
        sub_list = sub_list.copy()
        start_time=time.process_time()
        mrge.sort(sub_list, cmpfunction)
        stop_time=time.process_time()
        elapsed_time_mseg = round((stop_time - start_time)*1000,2)
        return elapsed_time_mseg, sub_list
    else:
        return None

