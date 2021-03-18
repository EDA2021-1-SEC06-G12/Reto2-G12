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
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from datetime import datetime
from DISClib.Algorithms.Sorting import shellsort as shes
from DISClib.Algorithms.Sorting import mergesort as mrge
from DISClib.Algorithms.Sorting import quicksort as quck
from DISClib.Algorithms.Sorting import insertionsort as inss


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    return model.initCatalog()

def loadData(catalog):
    videosfile = cf.data_dir + 'videos-large.csv'
    input_file = csv.DictReader(open(videosfile, encoding='utf-8'))
    for video in input_file:
        video["trending_date"] = datetime.strptime(video["trending_date"],"%y.%d.%m").date()
        model.addVideo(catalog, video)
    
    categoriesfile = cf.data_dir + "category-id.csv"
    i_file = csv.DictReader(open(categoriesfile, encoding='utf-8'), delimiter='\t')
    for category in i_file:
        model.addCategory(catalog,category)

def mejoresVideosPorViews(catalog, size):
    return model.sortVideos(catalog,size,cmpVideosbyViews)


def R1(categoria,pais,num,catalog):
    ID=model.categoriaporID(categoria,catalog)
    if ID==None:
        return 'Categoría no válida'
    else:
        l=model.lporcyp(ID,pais,catalog['videos'])
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
    l1 = model.lporpais(pais,catalog['videos'])
    if l1==None:
        return 'No hay información para este país.'
    else:
        l2 = model.sortVideos(l1,lt.size(l1),model.cmpVideosbyTitleandDate)[1]
        tupla=model.maxrep('title',l2)
        return '\nInformación del video trending por más días en '+pais+':\ntitle: '+tupla[0]+'; channel_title: '+tupla[1]+'; country: '+tupla[3]+'; días: '+str(tupla[4])


def R3(categoria,rep,catalog):
    ID=model.categoriaporID(categoria,catalog)
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
