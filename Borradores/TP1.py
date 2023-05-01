import argparse, os, sys
import traceback

#un proceso hijo por cada linea de archivo
#cada hijo debe invertir una linea de texto
#manejo de errores
#los hijos escriben el pipe y luego el padre lo lee
#el padre muestra el resultado final

#hardcodeo la ruta
#esto en realidad debe ser pasado como argumento
name="/home/alumno/Python-ejercicios/holamundo"


#en esta funcion abro el archivo
def parenting():
    try:
        file=open(name, 'r')
        text = file.readlines()
        print(text)
        return text 
    except Exception as e:
        with open('errors.log', 'w') as f:
            f.write(str(e)) 
            f.write(traceback.format_exc())

#funcion que me crea n hijos para n lineas
def forking():
    text=parenting()
    for i in range(len(text)):     
        child_n = os.fork()
        if child_n==0:
            print(reverse(text[i]))
            #aqui agrego al pipe el retorno de reverse
            os._exit(0)

#funcion que invierte la cadena
def reverse(str_reverse):
    str_reverse=str_reverse[::-1]
    return str_reverse

#funcion que abre mi pipe
def open_pipe():
    pass
forking()