import os
import time
#inicializo matrices hardcodeadas
matrix2x2=[[1,2],[3,4]]
anothermatrix2x2=[[5,6],[7,8]]


my_fifo="/tmp/fifo"
#creo pipe
if not os.path.exists(my_fifo):
    os.mkfifo(my_fifo)

def father():
    #metodo del proceso padre
    list_to_sort=[]
    fifo_input=open(my_fifo,"r")
    
    for line in range (4):
        #remuevo del string los parentesis; primer y ultimo caracter
        str_to_tuple=str(fifo_input.readline())[:-2][1:]
        #convierto el string a tupla
        result = tuple(map(int,str_to_tuple.split(',')))
        #agrego la tupla resultante a una lista
        list_to_sort.append(result)

    #ordena mis tuplas, [1] siginifica que lo ordena por el segundo elemento
    list_to_sort.sort(key=lambda tup: tup[1])
    print(list_to_sort)
    #el padre finaliza el proceso con exit()porque ya tengo todos los hijos recibidos y ordenados 
    exit()    
def a():

    fifo=open(my_fifo,"w")
    #paso a string la tupla de retorno
    returnvalue=str((matrix2x2[0][0]*anothermatrix2x2[0][0]+matrix2x2[0][1]*anothermatrix2x2[1][0],1))
    #escribo en la fifo
    fifo.write(returnvalue+"\n")
    #cierro fifo
    fifo.close()

def b():
    #no tiene sentido comentar los sigueintes metodos hijos, ya que es lo mismo para los tres restantes
    fifo=open(my_fifo,"w")
    returnvalue=str((matrix2x2[0][0]*anothermatrix2x2[0][1]+matrix2x2[0][1]*anothermatrix2x2[1][1],2))
    fifo.write(returnvalue+"\n")
    fifo.close()


def c():

    fifo=open(my_fifo,"w")    
    returnvalue=str((matrix2x2[1][0]*anothermatrix2x2[0][0]+matrix2x2[1][1]*anothermatrix2x2[1][0],3))
    fifo.write(returnvalue+"\n")
    fifo.close()

def d():

    fifo=open(my_fifo,"w")     
    returnvalue=str((matrix2x2[1][0]*anothermatrix2x2[0][1]+matrix2x2[1][1]*anothermatrix2x2[1][1],4))
    fifo.write(returnvalue+"\n")
    fifo.close()
    
def process_creator():
    child1=os.fork()
    if child1==0:
        a()
        #points that the process's return is 0
        os._exit(0)
    child2=os.fork()    
    if child2==0:
        b()
        os._exit(0)   
    child3=os.fork()    
    if child3==0:
        c()
        os._exit(0)   
    child4=os.fork()    
    if child4==0:
        d()
        os._exit(0)
    
    #lo hago esperar hasta que todos los procesos hijos finalicen
    time.sleep(0.001) #Ĺes da 1 milesima de segundo a los hijos para que finalicen  
    father()        
if __name__== "__main__":
    process_creator()

