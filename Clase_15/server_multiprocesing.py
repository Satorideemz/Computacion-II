#Cristian Albornoz

#!/usr/bin/python3
import socket
import multiprocessing
import sys

def handle_client(client_socket, client_address):

    #Notifica que entro un cliente  
    sys.stdout.write("New client connected.\n")
    
    while True:
        try:
            #En esta parte el server revisa si hay datos para procesar en el pipe
            msg = client_socket.recv(1024)
            if not msg:
                break
            data = msg.decode().strip()
            sys.stdout.write(f"Received: {data}\n")
            #Cuando el cliente cierra la conexion el servidor lo despide
            if data == "exit":
                response = "\r\nGoodbye\r\n"
                client_socket.send(response.encode("utf-8"))
                sys.stdout.write(f"Client {str(client_address)} closed the connection\r\n")
                break
            #Caso contrario sigue pasando a mayuscula sus mensajes    
            else:
                response_msg = data.upper() + "\r\n"
                client_socket.send(response_msg.encode("utf-8"))
        #El programa procesa la salida de conexion del cliente
        except BrokenPipeError:
            sys.stdout.write("Client closed the connection\n")
            break
        #Manejo cualquier otro error que pueda surgir
        except Exception as e:
            sys.stderr.write(f"An error occurred: {str(e)}\n")
            break
    #Luego de que el cliente se fue, cierro la conexion
    client_socket.close()

def main():
    #Defino los sockets
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host_address = ""
    listening_port = 50001
    #Le asigno el puerto en el que va a escuchar
    server_socket.bind((host_address, listening_port))

    #Fijo el limite de hasta 5 conexiones en cola
    server_socket.listen(5)
    sys.stdout.write(f"Server listening on {host_address}:{listening_port}\n")
    
    #Voy añadiendo a una lista los procesos de clientes que se van conectando
    processes = []

    while True:
        #El servidor acepta el cliente que entra con su su socket que lo identifica
        client_socket, client_address = server_socket.accept()
        sys.stdout.write(f"Connected to {client_address}\n")

        initial_msg = 'Thanks for connecting\r\n'
        client_socket.send(initial_msg.encode('ascii'))

        #Por cada cliente se genera un nuevo proceso
        process = multiprocessing.Process(target=handle_client, args=(client_socket, client_address))
        process.start()
        processes.append(process)

if __name__ == "__main__":
    main()
