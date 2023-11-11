import socket
from PIL import Image
import io

def convert_to_grayscale_pillow(image_data):
    img = Image.open(io.BytesIO(image_data)).convert('L')
    return img

def start_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('127.0.0.1', 8085)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(1)
    print(f'Server is starting on {server_address}')

def handle_connection(client_address,client_socket):

    try:
        print(f'Connection from {client_address}')

        # Receive the data in small chunks
        data = b''
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            data += chunk

            # Check if the EOI marker is present
            if b'\xFF\xD9' in data:
                break

        # Parse the request
        request_lines = data.split(b'\r\n')
        method = request_lines[0].split(b' ')

        # Handle the request
        handle_request(method,data,client_socket)

    finally:
        # Clean up the connection
        client_socket.close()    


def handle_request(method,data,client_socket):
    try:
        if method[0] == b'POST':
            print(f'POST request received. Converting to grayscale...')

            # Find the start and end of the image data
            start_idx = data.find(b'\r\n\r\n') + 4
            end_idx = data.rfind(b'\xFF\xD9') + 2

            # Get the image data between start and end indices
            image_data = data[start_idx:end_idx]

            # Convert the received image to grayscale
            grayscale_image = convert_to_grayscale_pillow(image_data)

            # Send the grayscale image back to the client
            with io.BytesIO() as output:
                grayscale_image.save(output, format="JPEG")
                grayscale_data = output.getvalue()

            # Send the correct HTTP/1.1 response
            response = f'HTTP/1.1 200 OK\r\nContent-Length: {len(grayscale_data)}\r\n\r\n'.encode('utf-8')
            client_socket.sendall(response + grayscale_data)

            print('Grayscale image sent back to the client.')

    except Exception as e:
        print(str(e))
        response = b'HTTP/1.1 405 Method Not Allowed\r\nContent-Length: 22\r\n\r\n'
        error_message = b'Request refused by server\n'
        client_socket.sendall(response + error_message)



def start_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('127.0.0.1', 8082)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(1)
    print(f'Server is starting on {server_address}')

    while True:
        # Wait for a connection
        print('Waiting for a connection...')
        client_socket, client_address = server_socket.accept()
        #Handle the connection between server and client
        handle_connection(client_address,client_socket)

def main():
    start_server()

if __name__ == '__main__':
    main()