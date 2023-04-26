import sys
import argparse

parser=argparse.ArgumentParser(description="genera lista de numeros impares")
parser.add_argument("n",type=int,default=0,help="numero entero positivo")
args=parser.parse_args()


def lista_impar(n):
    lista=[]
    if n>0:
        if (n%2)==0:
            for i in range(int(n/2)):
                i=(2*(i+1))-1
                lista.append(i)
                
        else:
            for i in range(int(n/2)+1):
                i=(2*(i+1))-1
                lista.append(i)
    sys.stdout.write(str(lista))
    sys.stdout.write('\n')

lista_impar(args.n)

