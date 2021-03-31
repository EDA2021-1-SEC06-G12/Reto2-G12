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
from DISClib.DataStructures import mapentry as me
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
    catalog = {'videos': lt.newList(datastructure='ARRAY_LIST', cmpfunction=cmpInit),
               'categories': lt.newList(datastructure='ARRAY_LIST'),
               'map_categories': None,
               "map_categories_country": None,
               "map_countries": None}

    """
    Este indice crea un map cuya llave es la categoria
    """
    catalog["map_categories"] = mp.newMap(numelements=4, maptype="CHAINING",loadfactor=4.0,comparefunction=compareMapCategory)
    """
    Este indice crea un map cuya llave es (el país + categoria)
    """
    catalog["map_categories_country"] = mp.newMap(numelements=64, maptype="CHAINING",loadfactor=4.0,comparefunction=compareMapCategory)
    """
    Este indice crea un map cuya llave es el país 
    """
    catalog["map_countries"] = mp.newMap(numelements=4, maptype="CHAINING",loadfactor=4.0,comparefunction=compareMapCategory)

    return catalog
 

# Funciones para creacion de datos
def newCategory_name(category_name):
    entry = {'category_name': "", "videos": None}
    entry['category_name'] = category_name
    entry['videos'] = lt.newList('ARRAY_LIST', cmpVideosbyLikes)
    return entry

def newCategory_name_country(key):
    entry = {'category_name_country': "", "videos": None}
    entry['category_name_country'] = key
    entry['videos'] = lt.newList('ARRAY_LIST', cmpVideosbyLikes)
    return entry

def newCountry(country):
    entry = {'country': "", "videos": None}
    entry['country'] = country
    entry['videos'] = lt.newList('ARRAY_LIST', cmpVideosbyLikes)
    return entry

# Funciones para agregar informacion al catalogo
def addCategory(catalog,category):
    lt.addLast(catalog['categories'],category)

def addVideo(catalog,video):
    lt.addLast(catalog['videos'],video)
    addVideoCategory(catalog,video)
    addVideoCountry(catalog,video)
    addVideoCategoryCountry(catalog,video)
    

def addVideoCategoryCountry(catalog,video):
    """
    Esta funcion adiciona un video a la lista de videos que fueron trending en un país
    y categoria específica. Esto se guarda en un map donde la llave es la combinación
    país + nombre de la categoria y el valor es una lista de videos.
    
    Por ejemplo: FAKE LOVE fue trending en canada y es de categoria music
    entonces se agrega a la lista de una llave dada por country + category_name.
    """
    map_categories_country = catalog["map_categories_country"]
    category_id = video["category_id"]
    country = video["country"].lower().strip()
    category_name = category_name_dado_ID(video["category_id"],catalog).lower().strip()
    key = country + category_name

    existCategory_name_country = mp.contains(map_categories_country, key)

    if existCategory_name_country:
        entry = mp.get(map_categories_country, key)
        entry = entry["value"]
        lista = entry["videos"]
        lt.addLast(lista,video)
    else:
        new_entry = newCategory_name_country(key)
        mp.put(map_categories_country, key, new_entry)
        lt.addLast(new_entry["videos"],video)
    

def addVideoCategory(catalog,video):
    """
    Esta función adiciona un video a la lista de videos a una lista de videos
    de una categoria en especifica. Esto se guarda en un map donde la llave
    es el nombre de la categoria y el valor es la lista de videos.
    """
    map_categories = catalog['map_categories']
    category_id = video['category_id']
    
    if (category_id != ''):
        category_name = category_name_dado_ID(video["category_id"],catalog)
    else:
        category_name = "NA"

    existCategory_name = mp.contains(map_categories, category_name)

    if existCategory_name:
        entry = mp.get(map_categories, category_name)
        entry = entry["value"]
        lista = entry["videos"]
        lt.addLast(lista,video)
        
    else:
        category_entry = newCategory_name(category_name)
        mp.put(map_categories, category_name, category_entry)
        lt.addLast(category_entry["videos"],video)

def addVideoCountry(catalog,video):
    """
    Esta función adiciona un video a la lista de videos a una lista de videos
    de un país en especifico. Esto se guarda en un map donde la llave
    es el nombre del país y el valor es la lista de videos.
    """
    map_countries = catalog['map_countries']
    country = video['country']

    existCountry = mp.contains(map_countries, country)

    if existCountry:
        entry = mp.get(map_countries, country)
        entry = entry["value"]
        lista = entry["videos"]
        lt.addLast(lista,video)
        
    else:
        country_entry = newCountry(country)
        mp.put(map_countries, country, country_entry)
        lt.addLast(country_entry["videos"],video)
        
        


# Funciones de consulta
def category_name_dado_ID(id,catalog):
    """Recibe el ID y halla el nombre de la categoria asociada
        id: id de categoria
        catalog: catalog
    retorna:
        str: nombre de la categoria"""
    categorias = catalog["categories"]
    v=it.newIterator(categorias)
    while it.hasNext(v):
        x = it.next(v)
        if x["id"] == id:
            return x["name"]
    else:
        return "NA"



def ID_dado_category_name(name,catalog):
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

def compareMapCategory(category1,entry):
    category_entry = me.getKey(entry)
    if (category1 == category_entry):
        return 0
    elif (category1 > category_entry):
        return 1
    else:
        return 0


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

