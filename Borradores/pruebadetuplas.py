import argparse, os, sys


def hijo(i, texto, pw):
    fila = texto[i] 
    invertida = ""
    for a in range(len(fila)):
        invertida += fila[-1-a]

    with os.fdopen(pw, 'w') as w:
        w.write(invertida)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, required=True, help="Ruta del archivo.") 

    args = parser.parse_args()

    with open(args.f, 'r') as archivo:  #Se listan las filas del archivo
        texto = archivo.readlines()
        cant_filas = len(texto)

    pr,pw = os.pipe()                   #Creacion de la tuberia. 

    for i in range(cant_filas):         #Tantos hijo como filas en el archivo.
        id_hijo = os.fork()

        if id_hijo == 0:
            os.close(pr)                #Se cierra la lectura para el hijo
            hijo(i, texto, pw)
            sys.exit(0)                 #Muere el hijo

    os.close(pw)

    for i in range(cant_filas):
        os.wait()
    
    with os.fdopen(pr) as r:
        print(r.read())

    sys.exit(0)

if __name__=='__main__':
    main()