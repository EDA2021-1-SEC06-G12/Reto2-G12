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


def getvidsby(catalog,idc,parametro):
    x=mp.get(catalog[idc],parametro)
    if x:
        return me.getValue(x)['videos']
    else:
        return None


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


def diasolikes(catalog,mapa,diasolikes):
    info=None
    mayor=0
    llaves=mp.keySet(mapa)
    i=it.newIterator(llaves)
    while it.hasNext(i):
        llave=it.next(i)
        entry=mp.get(mapa,llave)
        value=me.getValue(entry)
        m=int(value[diasolikes])
        if m>mayor:
            mayor=m
            info=value['info']
    return info['title'],info,mayor


def tags(catalog,pais,tag):
    videos=getvidsby(catalog,'countries',pais)
    final=lt.newList(datastructure='SINGLE_LINKED')
    i=it.newIterator(videos)
    while it.hasNext(i):
        vid=it.next(i)
        if tag in vid['tags']:
            lt.addLast(final,vid)
    return final


def idporcategory(name,catalog):
    categorias=catalog['categories']
    i=1
    while i<=lt.size(categorias):
        c=lt.getElement(categorias,i)
        if name.lower() in (c['name']).lower():
            return c['id']
        i+=1



##########


# Funciones de consulta
def tabla_mas_trending(lista):
    tamano = lt.size(lista)
    map_trending = mp.newMap(numelements=6, maptype="CHAINING",loadfactor=4.0,comparefunction=compareMapTitle)
    n = 1
    print("tamaño lista" + str(lt.size(lista)))

    while n<=tamano:
        x = lt.getElement(lista,n)
        title = x['title']
        print(title)
        existTitle = mp.contains(map_trending, title)
        print(existTitle)

        if existTitle:
            entry = mp.get(map_trending, title)
            entry = entry["value"]
            lista = entry["fechasyvarios"]

            lista_a_adicionar = lt.newList(datastructure="ARRAY_LIST")
            lt.addLast(lista_a_adicionar,x["trending_date"])
            lt.addLast(lista_a_adicionar,x["title"])
            lt.addLast(lista_a_adicionar,x["channel_title"])

            lt.addLast(lista,lista_a_adicionar)
            n += 1
        
        elif not existTitle:
            video_fecha_entry = newVideo_fecha(title)
            mp.put(map_trending, title, video_fecha_entry)

            lista_a_adicionar = lt.newList(datastructure="ARRAY_LIST")
            lt.addLast(lista_a_adicionar,x["trending_date"])
            lt.addLast(lista_a_adicionar,x["title"])
            lt.addLast(lista_a_adicionar,x["channel_title"])

            lt.addLast(video_fecha_entry["fechasyvarios"],lista_a_adicionar)
            n += 1
        
        print("N = " + str(n))
        print("tamaño: " + str(tamano))
        

    print(mp.size(map_trending))
    return map_trending

def mas_trending(tabla):
    keys = mp.keySet(tabla)
    v = it.newIterator(keys)
    num_fecha_max = 0
    key = 0
    info = None
    while it.hasNext(v):
        x = it.next(v)
        entry = mp.get(tabla,x)
        entry = entry["value"]
        num_fecha = lt.size(entry["fechasyvarios"])
        if num_fecha>num_fecha_max:
            num_fecha_max = num_fecha
            key = x
            info = entry["fechasyvarios"]
    print(info)
    return key,num_fecha_max,info

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






def mayortrending(mapa,parametro,catalog):
    entry=mp.get(mapa,parametro)
    final=mp.newMap(numelements=23, maptype="PROBING",loadfactor=0.50,comparefunction=compareMapTitle)
    if entry!=None:
        videos=me.getValue(entry)
        i=it.newIterator(videos)
        while it.hasNext(i):
            vid=it.next(i)
            titulo=vid['title']
            fecha=vid['trending_date']
            if lt.isPresent(mp.keySet(final),titulo)==0:
                fechas=lt.newList(datastructure='ARRAY_LIST')
                lt.addLast(fechas,fecha)
                mp.put(final,titulo,fechas)
            else:
                entrada=mp.get(final,titulo)
                fechas=me.getValue(entrada)
                if lt.isPresent(fechas,fecha)==0:
                    lt.addLast(fechas,fecha)

        m=mp.keySet(final)
        print(lt.size(m))

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


def compareid(id1,id2):
    if (int(id1) == int(id2)):
        return 0
    elif (int(id1) > int(id2)):
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

