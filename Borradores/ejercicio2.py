import sys
import argparse

parser=argparse.ArgumentParser(description="repite una cadena n veces")
parser.add_argument("n",type=str,default="",help="cadena a repetir")
parser.add_argument("m",type=int,default=0,help="numero de veces que se va a repetir")
args=parser.parse_args()


def repetir_string (n,m):
        
        sys.stdout.write(n*m)
        sys.stdout.write('\n')

repetir_string(args.n,args.m)

