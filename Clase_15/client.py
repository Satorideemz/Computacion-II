
#Este codigo no es parte de la consigna, es solo para no tener que estar escribiendo
#en la terminal cada vez que queria hacer una prueba de funcionamiento
import socket

# Configura la dirección del servidor y el puerto al que te quieres conectar
server_address = '127.0.0.1'  # Cambia esto a la dirección del servidor
server_port = 50001  # Cambia esto al puerto del servidor

# Crea un socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conéctate al servidor
client_socket.connect((server_address, server_port))

# Envía mensajes al servidor
while True:
    message = input("Enter a message (type 'exit' to quit): ")
    client_socket.send(message.encode('utf-8'))
#Cuando el cliente escribe exit se desconeccta    
    if message == 'exit':
        break

# Recibe y muestra las respuestas del servidor
while True:
    data = client_socket.recv(1024)
    if not data:
        break
    print("Received: %s" % data.decode())

# Cierra el socket del cliente
client_socket.close()

