import os
import sys
import argparse


parser=argparse.ArgumentParser(description="cuenta cantidad de palabras y lineas")
parser.add_argument("name",type=str,default="",help="ruta del archivo a traer")
args=parser.parse_args()


#name="/home/alumno/Python-ejercicios/holamundo"
#ubicacion del archivo!!
name=args.name

fdr,fdw = os.pipe()
pid=os.fork()
file= open(name,"r")
for lines in file:
    codif = lines.encode("ascii")
    if pid==0: 
        os.write(fdw,codif)
        #os.close(fdw)        

    elif pid!=0:
        lines=os.read(fdr,8192)
 
        decoded_lines=lines.decode("ascii")
        contador_lineas=decoded_lines.count('\n')
        res = len(decoded_lines.split())
        contador_palabras=res
                
        sys.stdout.write("\n ") 
        print("La cantidad de lineas que tiene es: ",contador_lineas)
        sys.stdout.write("\n ") 
        print("La cantidad de palabras que tiene es: ",contador_palabras)
  
    

