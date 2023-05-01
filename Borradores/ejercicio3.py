import sys
import re
import argparse
import traceback


parser=argparse.ArgumentParser(description="cuenta cantidad de palabras y lineas")
parser.add_argument("name",type=str,default="",help="cadena a repetir")
args=parser.parse_args()

#name="/home/alumno/Python-ejercicios/holamundo"
#ubicacion del archivo de prueba!!


def loadfile(name):
    file= open(name,"r")
    contador_lineas=0
    contador_palabras=0
    try:
        for line in file:
            contador_lineas=contador_lineas+1
            quen = len(re.findall(r'\w+', line))
            contador_palabras=contador_palabras+quen
            print(line)
            #print (str(res))
        print("La cantidad de lineas que tiene es: ",contador_lineas)
        print("La cantidad de palabras que tiene es: ",contador_palabras)
        file.close()        
    except Exception as e:
        with open('errors.log', 'w') as f:
            f.write(str(e)) 
            f.write(traceback.format_exc())

def average_lenght(name):
    average=0
    aard=[]
    a=input("Desea saber la longitud promedio de las palabras?(y/n)")
    if a=="y":
        try:
            file= open(name,"r")
            for line in file:
                aard =aard+ line.split()
            for i in range(len(aard)):
                average=average+len(aard[i])/len(aard)
            print("El promedio de la longitud de palabras es: ",average)
        except Exception as e:
            with open('errors.log', 'w') as f:
                f.write(str(e)) 
                f.write(traceback.format_exc())

loadfile(args.name)
average_lenght(args.name)


