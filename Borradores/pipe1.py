import os

name="/home/alumno/Python-ejercicios/holamundo"
#ubicacion del archivo!!

fdr,fdw = os.pipe()

pid=os.fork()

if pid==0:
    os.close(fdw) #cierra buffer de escritura
    while True:
        leido=os.read(fdr,2024) #leo dentro del pipe
        if len(leido) ==0:
            break #el proceso finaliza cuando ya no queda mas que leer del pipe
        os.write(1,leido.upper())
    
  

    exit()
    




os.close(fdr) #cierra buffer de lectura
while True:
    leido=os.read(0,2024) #agrego a leido la entrada del buffer de teclado
    if len(leido) ==0:
        break
    os.write(fdw,leido)   #mando los datos que he leido al pipe 