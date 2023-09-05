#Cristian Albornoz

#!/usr/bin/python3
import socket
import threading
import sys

#Cada vez que entra un cliente, pasa por este manejador que procesa sus mensajes de entrada
def handle_client(connection):
    #Notifica que entro un cliente  
    sys.stdout.write("New client connected.\n")
    
    while True:
        
        try:
            #En esta parte el server revisa si hay datos para procesar en el pipe
            data = connection.recv(1024)
            if not data:
                break
            message = data.decode().strip()
            sys.stdout.write(f"Received data: {message}\n")
            #Cuando el cliente cierra la conexion el servidor lo despide
            if message == "exit":
                response = "Goodbye!"
            else:
            #Caso contrario sigue pasando a mayuscula sus mensajes    
                response = message.upper()

            connection.send(response.encode("utf-8"))

        #El programa procesa la salida de conexion del cliente
        except BrokenPipeError:
            sys.stdout.write("Client closed the connection\n")
            break
        #Manejo cualquier otro error que pueda surgir
        except Exception as e:
            sys.stderr.write(f"An error occurred: {str(e)}\n")
            break
    #Luego de que el cliente se fue, cierro la conexion
    connection.close()
    sys.stdout.write("Client connection closed.\n")

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

    while True:
        #El servidor acepta el cliente que entra con su su socket que lo identifica
        client_socket, client_address = server_socket.accept()
        sys.stdout.write(f"Connected to {client_address}\n")

        #Bienvenido!!
        initial_msg = 'Welcome to the server!\n'
        client_socket.send(initial_msg.encode('utf-8'))

        #Por cada cliente que entra, creo un nuevo hilo
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()
