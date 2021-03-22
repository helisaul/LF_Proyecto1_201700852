
import tkinter as tk
from tkinter import filedialog
from io import open
from tkinter import *
from tkinter import ttk
from graphviz import Digraph
import graphviz
from tkinter.filedialog import askopenfilename
import webbrowser
import os
import re
from time import sleep
from os import system, name
from datetime import datetime
now = datetime.now()

restaurante = ""
datosRestaurante = []

restaurante2 = ""
global datosRestaurante2
datosRestaurante2 = []
root = tk.Tk()
root.withdraw()

global lexema
lexema = []

global lexema2
lexema2 = []

global Cadena
Cadena = []

global Cadena2
Cadena2 = []

global listaErr
listaErr = []

global listaErr2
listaErr2 = []


global delimitador
delimitador = ["=",";",":","[","]","\'"]

global delimitador2
delimitador2 = [",","\'","%"]

global Contador
Contador = 0


class Datos:
    linea = " "
    Fichero = " "
    Contador = 0
    Texto = " "


def Cargar_Menu():
    global Contador
    arch = Datos()
    arch.Fichero = filedialog.askopenfilename(initialdir="/",
                                              filetypes=(
                                                  ("Text File", "*.txt"), ("All Files", "*.*")),
                                              title="Choose a file.")
    print(arch.Fichero) 
    try:
        with open(arch.Fichero, 'r',5,"utf-8") as arch.Texto:

            for arch.linea in arch.Texto.readlines():

                if arch.linea != 0:
                    Contador += 1

                Cadena.append(arch.linea)

        print()
        print("------Se han Cargo el archivo correctamente!------")
        print()
    except:
        print("El Archivo no existe, Intentelo de nuevo")

def Cargar_Orden():
    global Contador
    arch = Datos()
    arch.Fichero = filedialog.askopenfilename(initialdir="/",
                                              filetypes=(
                                                  ("Text File", "*.txt"), ("All Files", "*.*")),
                                              title="Choose a file.")
    print(arch.Fichero)
    try:
        with open(arch.Fichero, 'r',5,"utf-8") as arch.Texto:
 
            for arch.linea in arch.Texto.readlines():

                if arch.linea != 0: 
                    Contador += 1

                Cadena2.append(arch.linea)

        print()
        print("------Se han Cargo el archivo correctamente!------")
        print()
    except:
        print("El Archivo no existe, Intentelo de nuevo")


def Analisis_Menu():
    global Cadena

    valido = True
    a = ""
    tipo = ""
    fila = 0
    #pos = 0
    s = 0
    for lineas in Cadena:
        linea = lineas.rstrip()
        fila += 1
        pos = 0
        while pos < len(linea):
            #print(fila,pos,s)
            
            caracter = linea[pos]  
            #print(caracter,"textp")
            if s == 0:
                if caracter.isalpha():
                    tipo = "identificador"
                    s = 1
                    a = a + caracter
                    pos = pos + 1
                elif caracter.isdigit():
                    tipo = "numerico"
                    s = 5
                    a = a + caracter
                    pos = pos + 1
                elif caracter == "=" or caracter == ";" or caracter == ":" or caracter == "[" or caracter == "]":
                    
                    if caracter == "=":
                        lexema.append([caracter,fila,pos,"token_igual"])
                        
                    elif caracter == ";":
                        lexema.append([caracter,fila,pos,"token_puntoycoma"])
                        
                    elif caracter == ":":
                        lexema.append([caracter,fila,pos,"token_2puntos"])

                    elif caracter == "[":
                        lexema.append([caracter,fila, pos,"token_corchete_inicio"])
                    
                    elif caracter == "]":
                            lexema.append([caracter,fila,pos,"token_corchete_final"])
                    pos = pos + 1
                elif caracter == "\'":
                    pos = pos + 1
                    s = 2
                    
                else:
                    if not caracter.isspace():
                        listaErr.append([caracter,fila,pos,"caracter_desconocido"])
                    pos = pos + 1
                



            elif s == 1:
                if caracter.isalpha() or caracter.isdigit() or caracter == "_":
                    a = a + caracter
                    pos = pos + 1
                else:
                    if  caracter in delimitador or caracter.isspace(): 
                        
                        if valido:
                            
                            lexema.append([a,fila, pos,"token_identificador"])
                           
                        else:
                            listaErr.append([a,fila,pos,"identificador no valido"])
                        s  = 0
                        a = "" 
                        valido = True
                    else:
                        valido = False
                        a = a + caracter
                        pos = pos + 1 
                    
            elif s == 2:
                if caracter == "\'": 
                    #a = a + caracter
                    
                    lexema.append([a,fila, pos,"token_cadena"])
                    pos = pos + 1 
                    a = ""
                    s = 0
                else:

                    a = a + caracter
                    pos = pos + 1
                    
            elif s == 5:
                if caracter.isdigit():
                    a = a + caracter
                    pos = pos + 1
                elif caracter == ".":
                    a = a + caracter
                    pos = pos + 1
                    s = 6
                else:
                    if  caracter in delimitador or caracter.isspace(): 
                        
                        if valido:
                            
                            lexema.append([a,fila, pos,"token_numero"])
                           
                        else:
                            listaErr.append([a,fila,pos,"numero  no valido"])
                        s  = 0
                        a = "" 
                        valido = True
                    else:
                        valido = False
                        a = a + caracter
                        pos = pos + 1 
            elif s == 6:
                if caracter.isdigit():
                    a = a + caracter
                    pos = pos + 1
                else:
                    if  caracter in delimitador or caracter.isspace(): 
                        
                        if valido:
                            
                            lexema.append([a, fila, pos,"token_numero"])
                           
                        else:
                            listaErr.append([a,fila,pos,"numero  no valido"])
                        s  = 0
                        a = "" 
                        valido = True
                    else:
                        valido = False
                        a = a + caracter
                        pos = pos + 1 
            if pos == len(linea):
                if a :
                    if s == 2:
                        listaErr.append([a,fila,pos,"cadena_incompleta"])
                    else:
                        if valido:
                         lexema.append([a,fila,pos,tipo])
                        else:
                            listaErr.append([a,fila,pos,tipo])
            
    
    for x in listaErr:
        print(x)
    print()
    
    #if  len(listaErr) > 0:



    for i in lexema:
        print(i)

def Analisis_Orden():
    global Cadena2
    
    fila = 0
    a = ""
    valido = True
    tipo = ""
    for lineas in Cadena2:
        linea = lineas.rstrip()
        fila +=1
        pos = 0
        s = 0
        while pos < len(linea):
            #print(fila,pos)
            caracter = linea[pos]
            
            #print(caracter,"texto")
            if s == 0:
                if caracter.isalpha():
                    tipo = "identificador"
                    s = 1
                    a = a + caracter
                    pos = pos + 1
                elif caracter.isdigit():
                    tipo = "numerico"
                    s = 5
                    a = a + caracter
                    pos = pos + 1
                elif caracter == "%" or caracter == ",":
                    if caracter == "%":
                        lexema2.append([caracter,fila,pos,"Descuento"])
                    elif caracter == ",":
                        lexema2.append([caracter,fila,pos,"separador_coma"])
                    pos = pos + 1
                
                elif caracter == "\'":
                    s = 2
                    pos = pos + 1
                        
                else:
                    if not caracter.isspace():
                        listaErr2.append([caracter,fila,pos,"caracter_desconocido"])
                    pos = pos + 1
            
            elif s == 1:
                if caracter.isalpha() or caracter.isdigit() or caracter == "_":
                    a = a + caracter
                    pos = pos + 1
                else:
                    if  caracter in delimitador2 or caracter.isspace(): 
                         
                        if valido:
                            
                            lexema2.append([a,fila, pos,"identificador"])
                           
                        else:
                            listaErr2.append([a,fila,pos,"identificador no valido"])
                        s  = 0
                        a = "" 
                        valido = True
                    else:
                        valido = False
                        a = a + caracter
                        pos = pos + 1 
                
            elif s == 2:
                if caracter == "\'":
                    lexema2.append([a, fila, pos,"token_cadena"])
                    pos = pos + 1 
                    a = ""
                    s = 0
                else:
                    a = a + caracter
                    pos = pos + 1
            
            elif s == 5:
                if caracter.isdigit():
                    a = a + caracter
                    pos = pos + 1
                else:
                    if  caracter in delimitador2 or caracter.isspace(): 
                        
                        if valido:
                            
                            lexema2.append([a,fila, pos,"token_numero"])
                           
                        else:
                            listaErr2.append([a,fila,pos,"numero  no valido"])
                        s  = 0
                        a = "" 
                        valido = True
                    else:
                        valido = False
                        a = a + caracter
                        pos = pos + 1 

            if pos == len(linea):
                if a :
                    if s == 2: # 'Restaurante lFP'
                        listaErr2.append([a,fila,pos,"cadena_incompleta"])
                    else:
                        if valido:
                         lexema2.append([a,fila,pos,tipo])
                        
                        else:
                             listaErr2.append([a,fila,pos,tipo])
                a = ""
    
    for j in listaErr2: 
        print(j)
    print("")
    for i in lexema2:
        print(i)

def Generar_Html_Lexema():

    with  open('file.html', 'a') as html:
            html.write('<html>')
            html.write('<head>')
            html.write('<meta charset="iso-8859-1" />')
            html.write('<title>')
            html.write('Tokens')
            html.write('</title>')
            
            html.write('<style>')
            '''
            html.write('body {')
            html.write('color: #ff0000;')
            html.write('}') 
            '''
            html.write('.contenedor1 {')
            #html.write('background-color: silver;')
            html.write('width: 50% ;')
            html.write('height: 800px ;')
            html.write('margin: 0 auto ;')
            html.write('}')
            html.write('</style>') 
            
            html.write('</head>')
            html.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">')
            html.write('<body>')
            html.write('<h1>')
            html.write('<center>')
            html.write('REPORTE DE LOS DATOS INGRESADOS')
            html.write('</center>')
            html.write('</h1>')
            html.write('<br>')
            html.write('<br>')
            html.write('<br>')
            
            html.write('<div class = "contenedor1">')
            html.write('<h2><center>Lista de Tokens</center></h2>')
            html.write('<table class = "table" >') 
            html.write('<thead class="thead-dark">') 
            html.write('<tr>')
            html.write('<th><strong>No.</strong></th>')
            html.write('<th><strong>Lexema</strong></th>')
            html.write('<th><strong>Fila</strong></th>')
            html.write('<th><strong>Columna</strong></th>')
            html.write('<th><strong>Token</strong></th>')
            html.write('</tr>')
            html.write('</thead>')
            global lexema
            contador = 0
            for i in lexema:
                    contador +=1
                    html.write('<tbody>')
                    html.write('<tr>')
                    html.write('<td>')
                    html.write(str(contador))
                    html.write('</td>')
                    html.write('<td>')
                    html.write(str(i[0]))
                    html.write('</td>')
                    html.write('<td>')
                    html.write(str(i[1]))
                    html.write('</td>')
                    html.write('<td>')   
                    html.write(str(i[2]))
                    html.write('</td>')
                    html.write('<td>')   
                    html.write(str(i[3]))
                    html.write('</td>')
                    html.write('</tr>')
                    html.write('<tbody>')
            html.write('</table>') 
            html.write('<h2><center>Lista de errores</center></h2>') 
            html.write('<table class = "table">')
            html.write('<thead class="thead-dark">')
            html.write('<tr>')
            html.write('<th><strong>No.</strong></th>')
            html.write('<th><strong>Fila</strong></th>')
            html.write('<th><strong>Columna</strong></th>')
            html.write('<th><strong>caracter</strong></th>')
            html.write('<th><strong>Descripcion</strong></th>')
            html.write('</tr>')
            html.write('</thead>')
            global listaErr
            cont = 0
            for j in listaErr:
                    cont += 1
                    html.write('<tr>')
                    html.write('<td>')
                    html.write(str(cont))
                    html.write('</td>')
                    html.write('<td>')
                    html.write(str(j[1]))
                    html.write('</td>')
                    html.write('<td>')
                    html.write(str(j[2]))
                    html.write('</td>')
                    html.write('<td>')
                    html.write(str(j[0]))
                    html.write('</td>')
                    html.write('<td>')
                    html.write(str(j[3]))
                    html.write('</td>')


                    html.write('</tr>')
                    

               
                    
            
            html.write('</table>')
            html.write('<center>') 
            html.write('<button onclick="javascript:window.print()" type="button" class="btn btn-danger">Imprimir</button>')
            html.write('</center>') 
            html.write('</div>')
            html.write('</body>')
            html.write('</html>')    
            html.close()
            os.system('file.html')

def analisisDeDatos(lista):
    global datosRestaurante
    pos = 0
    errores = False
    fase_analisis = 1
    seccion = [] # [seccion, productos]
    productos = [] # [prodTemp1, prodTemp2]
    prodTemp = [] # [id, nombre, precio, descripción]
    while pos < len(lista):
        #token_data = lista[pos] #Se captura el conjunto de datos de un token
        if fase_analisis == 1:
            if lista[pos][3] == "token_identificador":
                pos = pos + 1
                if lista[pos][3] == "token_igual": 
                    pos = pos + 1
                    if lista[pos][3] == "token_cadena":
                        global restaurante
                        restaurante = lista[pos][0]
                        #print("Nombre del restaurante:",lista[pos][0])
                        pos = pos + 1
                        fase_analisis = 2
                    else:
                        errores = True
                        #print("Error,", lista[pos][0], " no es una cadena")
                        break
                else:
                    errores = True
                    #print("Error,", lista[pos][0], " no es el simbol igual")
                    break
            else:
                errores = True
                #print("Error,", lista[pos][0], " no es un identificador")
                break
        elif fase_analisis == 2:
            if len(productos) > 0:
                seccion.append(productos.copy()) # seccion = ["Bebidas", [ prodTemp1, prodTemp2 ]]
                datosRestaurante.append(seccion.copy())
                productos.clear()
                seccion.clear()
            if lista[pos][3] == "token_cadena":
                pos = pos + 1
                if lista[pos][3] == "token_2puntos": 
                    seccion.append(lista[pos-1][0]) # seccion = ["Desayunos"]
                    #print("Nombre de seccion:",lista[pos-1][0])
                    pos = pos + 1
                    fase_analisis = 3
                else:
                    #print("Error,", lista[pos][0], " no es el simbolo dos puntos")
                    errores = True
                    break
            else:
                errores = True
                #print("Error,", lista[pos][0], " no es una cadena")
                break
        elif fase_analisis == 3:
            if lista[pos][3] == "token_corchete_inicio":
                pos = pos + 1
                if lista[pos][3] == "token_identificador":
                #agregar a la lista prodTemp (Evaluar en cascada)
                    prodTemp.append(lista[pos][0]) # prodTemp = ["bebida_1"]
                    pos = pos + 1
                    if lista[pos][3] == "token_puntoycoma":
                        pos = pos + 1
                        if lista[pos][3] == "token_cadena":
                            prodTemp.append(lista[pos][0]) # prodTemp = ["bebida_1", "Bebida #1"]
                            pos = pos + 1
                            if lista[pos][3] == "token_puntoycoma":
                                pos = pos + 1
                                if lista[pos][3] == "token_numero":
                                    prodTemp.append(lista[pos][0]) # prodTemp = ["bebida_1", "Bebida #1", "11."]
                                    pos = pos + 1
                                    if lista[pos][3] == "token_puntoycoma":
                                        pos = pos + 1
                                        if lista[pos][3] == "token_cadena":
                                            prodTemp.append(lista[pos][0]) # prodTemp = ["bebida_1", "Bebida #1", "11.","Descripcion Bebida 1"]
                                            pos = pos + 1
                                            if lista[pos][3] == "token_corchete_final":
                                                #agregar a lista productos prodTemp (.copy())
                                                productos.append(prodTemp.copy())
                                                prodTemp.clear()
                                                pos = pos + 1
                                                try:
                                                    if lista[pos][3] != "token_corchete_inicio":
                                                        fase_analisis = 2
                                                except:
                                                    break
                                            else:
                                                errores = True
                                                break
                                        else:
                                            errores = True
                                            break
                                    else:
                                        errores = True
                                        break
                                else:
                                    errores = True
                                    break
                            else:
                                errores = True
                                break
                        else:
                            errores = True
                            break
                    else:
                        errores = True
                        break
                else:
                    errores = True
                    break
            else:
                errores = True
                break
    if len(productos) > 0:
        seccion.append(productos.copy()) # seccion = ["Bebidas", [ prodTemp1, prodTemp2 ]]
        datosRestaurante.append(seccion.copy())
        productos.clear()
        seccion.clear()
    if errores:
        #generar el html
        print("Se detectó un error sintactico")
    else:
        print("Salio bien")

def analisisDeDatos2(lista):

    global datosRestaurante2
    pos = 0
    errores = False
    fase_analisis = 1
    seccion = [] # [seccion, productos]
    productos = [] # [prodTemp1, prodTemp2]
    descuento = [] # 
    prodTemp = [] # [id, nombre, precio, descripción]
    while pos < len(lista):

        #token_data = lista[pos] #Se captura el conjunto de datos de un token
        if fase_analisis == 1:
            if len(prodTemp) > 0:
                 productos.append(prodTemp.copy())
                 datosRestaurante2.append(productos.copy())
                 prodTemp.clear()
                 productos.clear()
                 
            if lista[pos][3] == "token_cadena":
                datosRestaurante2.append(lista[pos][0])
                #print(datosRestaurante2)
                pos = pos + 1
                if lista[pos][3] == "separador_coma":
                       pos = pos + 1
                       if lista[pos][3] == "token_cadena":
                           datosRestaurante2.append(lista[pos][0])
                           pos = pos + 1
                           if lista[pos][3] == "separador_coma":
                               pos = pos + 1
                               if lista[pos][3] == "token_cadena":
                                   datosRestaurante2.append(lista[pos][0]) 
                                   pos = pos + 1
                                   if lista[pos][3] == "separador_coma":
                                       pos = pos + 1
                                       if lista[pos][3]== "token_numero":
                                          datosRestaurante2.append(lista[pos][0])
                                          pos = pos + 1
                                          if lista[pos][3] == "Descuento":
                                            #print(datosRestaurante2)
                                            pos = pos + 1
                                            fase_analisis = 2
                                          else:
                                                errores = True
                                            #print("Error,", lista[pos][0], " no es una cadena")
                                                break
                                       else:
                                            errores = True
                                            #print("Error,", lista[pos][0], " no es una cadena")
                                            break
                                   else:
                                        errores = True
                                            #print("Error,", lista[pos][0], " no es una cadena")
                                        break
                               else:
                                    errores = True
                                            #print("Error,", lista[pos][0], " no es una cadena")
                                    break
                           else:
                                errores = True
                                            #print("Error,", lista[pos][0], " no es una cadena")
                                break
                       else:
                            errores = True
                                            #print("Error,", lista[pos][0], " no es una cadena")
                            break
                else:
                    errores = True
                                            #print("Error,", lista[pos][0], " no es una cadena")
                    break
            else:
                errores = True
                                            #print("Error,", lista[pos][0], " no es una cadena")
                break
        elif fase_analisis == 2:
             if lista[pos][3] == "token_numero":
                prodTemp.append(lista[pos][0])
                pos = pos + 1
                if lista[pos][3] == "separador_coma":
                    pos = pos + 1
                    if lista[pos][3]== "identificador":
                     prodTemp.append(lista[pos][0])
                     productos.append(prodTemp.copy())
                     prodTemp.clear()
                        #fase_analisis = 2
                     pos = pos +1    
    if len(productos) > 0:
        #productos.append(prodTemp.copy())
        datosRestaurante2.append(productos.copy())
        prodTemp.clear()
        productos.clear()

def AnalisisSemantico():

            try:
                analisisDeDatos(lexema)
            except:
                print("Error de lectura")


            print("Nombre del restaurante:", restaurante)
            for seccion in datosRestaurante:
                print("Seccion:",seccion[0])
                for productos in seccion[1]:
                    print("\t\tDatos:", productos)
def Generar_Html_para_Menu():

     with  open('file2.html', 'a') as html:
            html.write('<html>')
            html.write('<head>')
            html.write('<meta charset="iso-8859-1" />')
            html.write('<title>')
            html.write('Menu')
            html.write('</title>')
            
            html.write('<style>')
            '''
            html.write('body {')
            html.write('color: #ff0000;')
            html.write('}') 
            '''
            html.write('.contenedor1 {')
            #html.write('background-color: silver;')
            html.write('width: 45% ;')
            html.write('height: 800px ;')
            html.write('margin: 0 auto ;')
            html.write('border-radius: 10px;')
            html.write('}')
            html.write('</style>') 
            
            html.write('</head>')
            html.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">')
            html.write('<body>')
            html.write('<h1>')
            html.write('<center>')
            html.write(str(restaurante))
            html.write('</center>')
            html.write('</h1>')
            html.write('<br>')
            html.write('<br>')
            html.write('<br>')
            
            html.write('<div class = "contenedor1">')
            html.write('<h2><center>Menú</center></h2>')
            html.write('<table class = "table" >') 
            html.write('<thead bgcolor="crimson" >') 
            html.write('<tr>')
            html.write('<th><strong></strong></th>')
            html.write('<th><strong>Precios</strong></th>')
            html.write('</tr>')
            html.write('</thead>')
            for seccion in datosRestaurante:
                   
                    html.write('<tbody width="50%" >')
                    html.write('<tr>')
                    html.write('<td>')
                    html.write('<h3>')
                    html.write(str(seccion[0]))
                    html.write('</h3>')
                    html.write('</td>')
                    html.write('</tr>')
                    html.write('<tbody>')
                    for productos in seccion[1]: 
                        html.write('<tbody>')
                        html.write('<tr>')
                        html.write('<td width="35%">')
                        html.write(str(productos[1]))
                        html.write('</td>')
                        html.write('<td>')
                        html.write('Q')
                        html.write(str(float(productos[2])))
                        html.write('</td>')
                        html.write('</tr>')
                        html.write('<tr>')
                        html.write('<td>')
                        html.write(str(productos[3]))
                        html.write('</td>')
                        html.write('</tr>')
                        html.write('<tbody>')

            html.write('</table>')
            html.write('<center>') 
            html.write('<button onclick="javascript:window.print()" type="button" class="btn btn-danger">Imprimir</button>')
            html.write('</center>')  
            html.write('</div>')
            html.write('</body>')
            html.write('</html>')    
            html.close()
            os.system('file2.html')


def AnalisisSemantico2():
            try:
                analisisDeDatos2(lexema2)
            except:
                print("Error de lectura")
            print("")
            print(datosRestaurante2)
def Procesar_Menu():
#Que necesitamos???
#1.datosRestaurante
#2.datosRestaurante2
      with  open('file3.html', 'a') as html:
            html.write('<html>')
            html.write('<head>')
            html.write('<meta charset="iso-8859-1" />')
            html.write('<title>')
            html.write('Menu')
            html.write('</title>')
            
            html.write('<style>')
            '''
            html.write('body {')
            html.write('color: #ff0000;')
            html.write('}') 
            '''
            html.write('.contenedor1 {')
            html.write('width: 45% ;')
            html.write('height: 800px ;')
            html.write('margin: 0 auto ;') 
            html.write('border-radius: 10px;')
            html.write('}')
            html.write('.contenedor2 {')
            html.write('width: 45% ;')
            html.write('height: 130px ;')
            html.write('margin: 0 auto ;') 
            #html.write('background-color: #00FF00;') 

            html.write('border-radius: 10px;')
            html.write('}')



            html.write('</style>') 
            contador = 1
            html.write('</head>')
            html.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">')
            html.write('<body>')
            html.write('<h4>')
            html.write('<center>')
            html.write(str(restaurante))
            html.write('<br>')
            html.write('Factura No.')
            html.write(str(contador))
            html.write('<br>')
            html.write('Fecha :')
            html.write(str(now.year))
            html.write('/')
            html.write(str(now.month))
            html.write('/')
            html.write(str(now.day ))
            html.write('<br>')
            html.write('Hora de impresion :')
            html.write(str(now.hour))
            html.write(':')
            html.write(str(now.minute))
            html.write(':')
            html.write(str(now.second))
            html.write('<br>')

            html.write('</center>')
            html.write('</h4>')
            html.write('<br>')
            html.write('<br>')
            html.write('<br>')
            html.write('<br>')
            html.write('<div class = "contenedor2">')
            html.write('<h5>')
            html.write('Datos del Cliente')
            html.write('<br>')
            html.write('Nombre: ')
            html.write(str(datosRestaurante2[0]))
            html.write('<br>')
            html.write('Nit: ')
            html.write(str(datosRestaurante2[1]))
            html.write('<br>')
            html.write('Direccion: ')
            html.write(str(datosRestaurante2[2]))
            html.write('</h5>')
            html.write('</div>')
            html.write('<div class = "contenedor1">')
            html.write('<h5>Descripcion</h5>')
            html.write('<table class = "table" >') 
            html.write('<thead bgcolor="crimson" >') 
            html.write('<tr>')
            html.write('<th><strong>Cantidad</strong></th>')
            html.write('<th><strong>Concepto</strong></th>')
            html.write('<th><strong>Precio</strong></th>')
            html.write('<th><strong>Total</strong></th>')
            html.write('</tr>')
            html.write('</thead>')
            valido = True
            a = 0
            for seccion in datosRestaurante:
                #print("Seccion:",seccion[0])
                for productos in seccion[1]:
                    #rint("\t\tDatos:", productos[0])
                    
                    for i in datosRestaurante2[4]:
                        if productos[0] in i:
                         if valido:
                            
                            x = float(i[0])
                            y = float(productos[2])
                            rest = float(x*y)
                            a = a + rest
                            pro = ((float(datosRestaurante2[3]))/100)
                            pro2 = 100*pro
                            pro3 = pro2 + a
                            #print(productos[0],"el resultado es : ",rest)
                            html.write('<tbody>')
                            html.write('<tr>')
                            html.write('<td>')
                            html.write(str(i[0]))
                            html.write('</td>')
                            html.write('<td>')
                            html.write(str(productos[1]))
                            html.write('</td>')
                            html.write('<td>')
                            html.write(str(float(productos[2])))
                            html.write('</td>')
                            html.write('<td>')
                            html.write('Q')
                            html.write(str(rest))
                            html.write('</td>')
                            html.write('</tr>')
            html.write('<tbody>')
            html.write('<tbody>') 
            html.write('<tr>')
            html.write('<td>')
            html.write('Sub Total')
            html.write('</td>')
            html.write('<td>')
            html.write('')
            html.write('</td>')
            html.write('<td>')
            html.write('')
            html.write('</td>')
            html.write('<td>')
            html.write('Q')
            html.write(str(a))
            html.write('</td>')
            html.write('</tr>')
            html.write('<tr>')
            html.write('<td>')
            html.write('Propina')
            html.write('')
            html.write('(')
            html.write(str(datosRestaurante2[3]))
            html.write('')
            html.write('%')
            html.write(')')
            html.write('</td>')
            html.write('<td>')
            html.write('')
            html.write('</td>')
            html.write('<td>')
            html.write('')
            html.write('</td>')
            html.write('<td>')
            html.write('Q')
            html.write(str(pro2))
            html.write('</td>')
            html.write('</tr>')
            html.write('</tbody>') 

            html.write('<tbody>') 
            html.write('<tr>')
            html.write('<td>')
            html.write('Total ')
            html.write('</td>')
            html.write('<td>')
            html.write('')
            html.write('</td>')
            html.write('<td>')
            html.write('')
            html.write('</td>')
            html.write('<td>')
            html.write('Q')
            html.write(str(pro3))
            html.write('</td>')
            html.write('</tr>')
            html.write('</tbody>')    
            html.write('</table>') 
            html.write('<center>') 
            html.write('<button onclick="javascript:window.print()" type="button" class="btn btn-danger">Imprimir</button>')
            html.write('</center>') 
            html.write('</div>')
            html.write('</body>')
            html.write('</html>')    
            html.close()
            os.system('file3.html')   


        
             

def Generar_Grafo():
    w = Digraph()
    
    w.edges((restaurante, str(seccion[0])) for seccion in datosRestaurante)
    
    w.view()  
    '''
    dot = Digraph(comment='The Test Table')

    # Agregue el punto A, la etiqueta de A es el punto A
    dot.node('A', restaurante)
    for seccion in datosRestaurante:
    # Agregue el punto B, la etiqueta de B es el punto B
        dot.node('B', seccion[0]) 
        for productos in seccion[1]:
            dot.node('C',productos[0])

    # dot.view()

    # Agrega un punto C, la etiqueta de C es el punto C
    #dot.node('C', 'Dot C')
        # dot.view()

        # Cree un montón de aristas, es decir, dos aristas que conectan AB y una arista que conecta AC.
        dot.edges(['AB','BC'])
        # dot.view()

        # Crea un borde entre dos puntos
    #dot.edge('B', 'C', 'test')
    # dot.view()


    # Obtenga la forma de cadena del código fuente de DOT
    print(dot.source) 
    # // The Test Table
    # digraph {
    #   A [label="Dot A"]
    #   B [label="Dot B"]
    #   C [label="Dot C"]
    #   A -> B
    #   A -> C
    #   A -> B
    #   B -> C [label=test]
    # }


    # Guarde la fuente en el archivo y proporcione el motor Graphviz
    dot.render('test-output/test-table.gv', view=True)
   '''

def Salir():
    return exit


def Menu():
    global datosRestaurante2
    opcion = 0
    while opcion != 6:
        print("")
        print("1. Cargar Menu")
        print("2. Cargar Orden")
        print("3. Generar Menu")
        print("4. Generar Factura")
        print("5. Genera Arbol")
        print("6. Salir")
        print(">> Ingrese una opcion :")
        opcion = int(input(">> "))
        print("")
        if opcion == 1:
            Cargar_Menu()
            Analisis_Menu()
            AnalisisSemantico()
            Generar_Html_Lexema()
           
        elif opcion == 2:
            Cargar_Orden()
            Analisis_Orden()
            AnalisisSemantico2()
        elif opcion == 3:
            #analisisDeDatos2(lexema2)
            Generar_Html_para_Menu()

        elif opcion == 4:
            
            Procesar_Menu()
        elif opcion == 5:
            Generar_Grafo()
        elif opcion == 6:
            Salir()
        else:
            print("Ingrese una de la opciones que hay en menu")


Menu()
