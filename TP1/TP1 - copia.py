import argparse, os
import traceback

#en esta funcion abro el archivo y lo escribo en pipe
def parenting(name):
    pipes=[]
    try:
        file=open(name, 'r')
        text = file.readlines()
        #por cada linea de texto leida genero un pipe para cada proceso
        for i in range(len(text)):
            pipe_r,pipe_w = os.pipe()
            write_pipe(text[i],pipe_w)
            pipes.append((pipe_r,pipe_w))
            
        return pipes 
    except Exception as e:
        with open('errors.log', 'w') as f:
            f.write(str(e)) 
            f.write(traceback.format_exc())

#funcion que me crea n hijos para n lineas
def forking(pipes, mainpipe_w):
    children = []
    for i in range(len(pipes)):
        # create a unique identifier for each line
        line_id = i + 1
        # create a child process
        child_n = os.fork()
        if child_n == 0:
            # receive the line from the parent process
            received_text = read_pipe(pipes[i][0])
            # reverse the line
            received_text = reverse(received_text)
            # send the reversed line to the parent process
            write_pipe(f"{line_id}:{received_text}", mainpipe_w)
            # exit the child process
            os._exit(0)
        else:
            # save the child process id and line id in a tuple
            children.append((child_n, line_id))

    # wait for all child processes to finish
    for child in children:
        os.waitpid(child[0], 0)

    # sort the lines based on their unique identifier
    sorted_lines = sorted([read_pipe(mainpipe_r).strip() for mainpipe_r, _ in pipes], key=lambda x: int(x.split(":")[0]))

    # join the lines and return the reversed text
    return "\n".join([x.split(":")[1] for x in sorted_lines[::-1]])


#funcion que invierte la cadena
def reverse(str_reverse):
    str_reverse=str_reverse[::-1]
    return str_reverse

#funcion que se usa para escribir en el pipe
def write_pipe(encodetext,writingpipe):
    try:
        encodetext=encodetext.encode("ascii")
        os.write(writingpipe,encodetext)

    except Exception as e:
        with open('errors.log', 'w') as f:
            f.write(str(e)) 
            f.write(traceback.format_exc())

#funcion que se usa para leer un pipe   
def read_pipe(readingpipe):
    try:
        reading=os.read(readingpipe,8192)
        reading=reading.decode("ascii")
        return reading
    except Exception as e:
        with open('errors.log', 'w') as f:
            f.write(str(e)) 
            f.write(traceback.format_exc())

def main():
    #ruta hardcodeada
    #name="/home/cristian/python-ejercicios/Ejercicios/TP1/holamundo"
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, required=True, help="Insert textfile path")
    args = parser.parse_args() 
    #defino pipe que me devolveran los hijos
    mainpipe_r,mainpipe_w=os.pipe()  
    #realizo tareas paternas
    forking(parenting(args.f),mainpipe_w)
    #espero a que los hijos terminen de ejecutar
    for i in range(len(parenting(args.f))):
        os.wait()

    #devolucion final del proceso padre
    print(read_pipe(mainpipe_r))

if __name__=='__main__':
    main()