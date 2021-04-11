﻿"""
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
from DISClib.Algorithms.Sorting import shellsort as shes
from DISClib.Algorithms.Sorting import insertionsort as inss
from DISClib.Algorithms.Sorting import selectionsort as sels
from DISClib.Algorithms.Sorting import mergesort as mrge
from DISClib.Algorithms.Sorting import quicksort as quck
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf


# Construccion de modelos
def initCatalog():
    catalog= {
            'videos': lt.newList(datastructure='ARRAY_LIST', cmpfunction=cmpInit),
            'categories': lt.newList(datastructure='ARRAY_LIST'),
            'ids': None,
            'countries': None}

    catalog['ids'] = mp.newMap(numelements=50, 
                                maptype="PROBING",
                                loadfactor=0.50,
                                comparefunction=comparemapid)

    catalog['countries'] = mp.newMap(numelements=100, 
                                    maptype="PROBING",
                                    loadfactor=0.50,
                                    comparefunction=comparemapcountry)

    return catalog



def newid(ide):
    entry={'id':0,'videos':None}
    entry['id']=ide
    entry['videos']=lt.newList()
    return entry

def newcountry(country):
    entry={'country':'','videos':None}
    entry['country']=country.lower()
    entry['videos']=lt.newList()
    return entry

def newtitle(title):
    entry={'title':'','dias':0,'likes':0,'info':None}
    entry['title']=title
    return entry

def newtviews(title):
    entry={'title':'','views':0,'info':None}
    entry['title']=title
    return entry

def addVideo(catalog,video):
    lt.addLast(catalog['videos'],video)
    addid(catalog,video['category_id'],video)
    addcountry(catalog,video['country'],video)


def addCategory(catalog,category):
    lt.addLast(catalog['categories'],category)


def addid(catalog,ide,video):
    ids=catalog['ids']
    existid=mp.contains(ids,ide)
    if existid:
        entry=mp.get(ids,ide)
        ID=me.getValue(entry)
    else:
        ID=newid(ide)
        mp.put(ids,ide,ID)
    
    lt.addLast(ID['videos'],video)


def addcountry(catalog,country,video):
    countries=catalog['countries']
    existcountry=mp.contains(countries,country)
    if existcountry:
        entry=mp.get(countries,country)
        value=me.getValue(entry)
    else:
        value=newcountry(country)
        mp.put(countries,country,value)
    lt.addLast(value['videos'],video)



#Devuelve la lista de videos de una llave específica en un mapa dado
def getvidsby(catalog,idc,parametro):
    x=mp.get(catalog[idc],parametro)
    if x:
        return me.getValue(x)['videos']
    else:
        return None



#Retorna una lista con los videos de un tag y país en especial
def tags(catalog,pais,tag):
    videos=getvidsby(catalog,'countries',pais)
    final=lt.newList(datastructure='SINGLE_LINKED')
    i=it.newIterator(videos)
    while it.hasNext(i):
        vid=it.next(i)
        if tag in vid['tags']:
            lt.addLast(final,vid)
    return final


#Recibe una lista de videos y devuelve un mapa cuyas llaves son los nombres de los videos y cuyo valor es una entrada de la función newtitle
def titleporidc(catalog,lista):
    mapa=mp.newMap()
    i=it.newIterator(lista)

    while it.hasNext(i):
        vid=it.next(i)
        tit=vid['title']
        existit=mp.contains(mapa,tit)
        if existit:
            entry=mp.get(mapa,tit)
            value=me.getValue(entry)
            if vid['likes']>value['likes']:
                value['likes']=vid['likes']
        else:
            value=newtitle(tit)
            mp.put(mapa,tit,value)
            value['info']=vid
            value['likes']=vid['likes']
        value['dias']+=1

    return mapa


#Devuelve un mapa con videos de un país y id en particular cuyas llaves son los títulos de los videos y cuyos valores son entradas de newtviews
def countryid(catalog,country,ide):
    videos=getvidsby(catalog,'countries',country)
    mapa=mp.newMap()
    i=it.newIterator(videos)
    while it.hasNext(i):
        vid=it.next(i)
        if vid['category_id']==ide:
            entry=newtviews(vid['title'])
            mp.put(mapa,vid['title'],entry)
            entry['views']=vid['views']
            entry['info']=vid
    return mapa



#Busca video con mayor número de dias/likes/views de un map con videos y retorna una tupla con (título del video, información video, valor mayor)
def dlv(catalog,mapa,dlv):
    info=None
    mayor=0
    llaves=mp.keySet(mapa)
    i=it.newIterator(llaves)
    while it.hasNext(i):
        llave=it.next(i)
        entry=mp.get(mapa,llave)
        value=me.getValue(entry)
        m=int(value[dlv])
        if m>mayor:
            mayor=m
            info=value['info']
    return info['title'],info,mayor


    

#Devuelve el ID dado el nombre de una categoría
def idporcategory(name,catalog):
    categorias=catalog['categories']
    i=1
    while i<=lt.size(categorias):
        c=lt.getElement(categorias,i)
        if name.lower() in (c['name']).lower():
            return c['id']
        i+=1


# Funciones utilizadas para comparar elementos dentro de una lista
def cmpInit(video1,video2):
    if int(video1["views"])==int(video2["views"]):
        return 0
    elif int(video1["views"])>int(video2["views"]):
        return 1
    else:
        return -1


def comparemapid(id, tag):
    identry = me.getKey(tag)
    if (int(id) == int(identry)):
        return 0
    elif (int(id) > int(identry)):
        return 1
    else:
        return -1

def comparemapcountry(name,tag):
    centry=me.getKey(tag)
    if (name == centry):
        return 0
    elif (name > centry):
        return 1
    else:
        return -1




