"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
import model
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
assert cf
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as mp

default_time = 1000
sys.setrecursionlimit(default_time*10)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenida/o")
    print("1- Cargar información en el catálogo")
    print("2- Consultar el número que se desee de videos con más views en el país y categoría de interés")
    print("3- Consultar el video tendencia por más días en el país que se desee")
    print("4- Consultar el video tendencia trending por más días en la categoría que se desee")
    print("5- Consultar el número que se desee de videos con más likes en el país y tag de interés")
    print("0- Salir")


catalog = None


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar: ')
    if int(inputs[0]) == 1:
        print('\nCargando información de los archivos...\n')
        catalog = controller.initCatalog()
        answer = controller.loadData(catalog)
        print("Se cargaron " + str(lt.size(catalog['videos'])) + " datos de video y " + str(lt.size(catalog['categories'])) + " de categorías.")
        v=lt.firstElement(catalog['videos'])
        print("\nInformación del primer video cargado \n" +"Título: "+v['title']+"\nTítulo del canal: "+v['channel_title']+"\nTrending date: "+str(v['trending_date'])+"\nPaís: "+v['country']+"\nVistas: "+v['views']+ "\nLikes: "+v['likes']+"\nDislikes: "+v['dislikes']+'\n')
        print("\nLista de categorías " + "\nID - Nombre")
        i=it.newIterator(catalog['categories'])
        while it.hasNext(i):
            x=it.next(i)
            print(str(x['id']) + " - " + str(x['name']))
        print('\n')
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
        print('\n') 
        input('Presione enter para continuar')

    elif int(inputs[0])==2:
        country=input('Ingrese el país: ').lower()
        category=input('Ingrese la categoría: ').lower()
        n=int((input('Ingrese el número: ')))
        answer = controller.req1(catalog,country,category,n)
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
        print('\n') 
        input('Presione enter para continuar')


    elif int(inputs[0])==3:
        country=input('Ingrese el país: ').lower()
        x=input('Desea organizar videos por... (0: título / 1: video ID): ')
        if x=='0':
            td='title'
        elif x=='1':
            td='video_id'
        else:
            print('Ingrese una opción válida (0,1)')
        answer = controller.req2(catalog,country,td)

        print('\n'+answer[0]+'\n')
        print("Tiempo [ms]: ", f"{answer[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[2]:.3f}")
        print('\n') 
        
        input('Presione enter para continuar')

    elif int(inputs[0])==4:
        category=input('Ingrese la categoría: ').lower()
        x=input('Desea organizar videos por... (0: título / 1: video ID): ')
        if x=='0':
            td='title'
        elif x=='1':
            td='video_id'
        else:
            print('Ingrese una opción válida (0,1)')
        answer = controller.req3(catalog,category,td)
        print('\n'+answer[0]+'\n')
        print("Tiempo [ms]: ", f"{answer[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[2]:.3f}")
        print('\n') 
        
        input('Presione enter para continuar')

    elif int(inputs[0])==5:
        country=input('Ingrese el país: ').lower()
        tag=input('Ingrese el tag: ').lower()
        n=int((input('Ingrese el número: ')))
        answer = controller.req4(catalog,country,tag,n)
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
        print('\n') 
        input('Presione enter para continuar')

    else:
        sys.exit(0)
sys.exit(0)
