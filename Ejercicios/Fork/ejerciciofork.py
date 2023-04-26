import os
import sys
import argparse

parser=argparse.ArgumentParser(description="devuelve raiz cuadrada de un numero")
parser.add_argument("-n",'--numero',type=float,default=0,help="numero positivo")
parser.add_argument("-f",'--fork',default=False, action='store_true',help="parametro fork")

args=parser.parse_args()
#si no se escribe el -f, solo mostrar la raiz positiva

def getsqroot():
    pid=os.fork()

    if (pid): #proceso padre
        sys.stdout.write('\n PADRE(PID %s)' % os.getpid())
        sys.stdout.write("\n raiz cuadrada positiva ") 
        sys.stdout.write(str(args.numero ** (1/2)))
        sys.stdout.write("\n ") 

    elif args.fork: #proceso hijo
        sys.stdout.write('\n HIJO(PID %s)' % os.getpid())
        sys.stdout.write("\n raiz cuadrada negativa ")    
        sys.stdout.write(str(-(args.numero ** (1/2))))
        sys.stdout.write("\n ")
        
if __name__ == "__main__":
    if args.numero==0:
        sys.stdout.write("raiz cuadrada 0 \n")
    else:
        getsqroot()