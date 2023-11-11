import socket
from PIL import Image
import io
import multiprocessing
import argparse

def convert_to_grayscale_pillow(image_data):
    img = Image.open(io.BytesIO(image_data)).convert('L')
    return img

def image_processing_child(pipe, event):
    while True:
        image_data = pipe.recv()
        if image_data == b'exit':
            # Exit the child process
            break

        grayscale_image = convert_to_grayscale_pillow(image_data)

        with io.BytesIO() as output:
            grayscale_image.save(output, format="JPEG")
            grayscale_data = output.getvalue()

        pipe.send(grayscale_data)

        # Notify the parent that the image conversion is complete
        event.set()

def handle_connection(client_socket, child_pipe, event):
    try:
        client_address = client_socket.getpeername()
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
        handle_request(method, data, client_socket, child_pipe, event)

    finally:
        # Clean up the connection
        client_socket.close()

def handle_request(method, data, client_socket, child_pipe, event):
    try:
        if method[0] == b'POST':
            print(f'POST request received. Converting to grayscale...')

            # Find the start and end of the image data
            start_idx = data.find(b'\r\n\r\n') + 4
            end_idx = data.rfind(b'\xFF\xD9') + 2

            # Get the image data between start and end indices
            image_data = data[start_idx:end_idx]

            # Send the image data to the child process
            child_pipe.send(image_data)

            # Wait for the child process to complete image conversion
            event.wait()

            # Receive the processed grayscale image data from the child process
            grayscale_data = child_pipe.recv()

            # Reset the event for the next connection
            event.clear()

            # Send the correct HTTP/1.1 response with the grayscale image data
            response = f'HTTP/1.1 200 OK\r\nContent-Length: {len(grayscale_data)}\r\n\r\n'.encode('utf-8')
            client_socket.sendall(response + grayscale_data)

            print('Grayscale image sent back to the client.')

    except Exception as e:
        print(str(e))
        response = b'HTTP/1.1 405 Method Not Allowed\r\nContent-Length: 22\r\n\r\n'
        error_message = b'Request refused by server\n'
        client_socket.sendall(response + error_message)

def start_server(ip, port):

    if ':' in ip:
        # Use socket.AF_INET6 for IPv6 addresses
        server_socket = socket.create_server((ip, port), family=socket.AF_INET6, dualstack_ipv6=True)
    else:
        # Use socket.AF_INET for IPv4 addresses
        server_socket = socket.create_server(('0.0.0.0', port))
    # Create an event for synchronization
    conversion_event = multiprocessing.Event()

    print(f'Server is starting on {server_socket.getsockname()}')

    while True:
        # Wait for a connection
        print('Waiting for a connection...')
        client_socket, _ = server_socket.accept()

        # Create a new child process for each connection
        child_pipe, parent_pipe = multiprocessing.Pipe()
        image_processing_process = multiprocessing.Process(
            target=image_processing_child, args=(child_pipe, conversion_event))
        image_processing_process.start()

        # Handle the connection between server and client
        handle_connection(client_socket, parent_pipe, conversion_event)

        # Send 'exit' signal to child process to terminate it
        parent_pipe.send(b'exit')
        image_processing_process.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tp2 - procesa imagenes')
    parser.add_argument('-i', '--ip', default='::', help='Direccion de escucha')
    parser.add_argument('-p', '--port', type=int, default=8080, help='Puerto de escucha')

    args = parser.parse_args()
    
    try:
        start_server(args.ip, args.port)
    except KeyboardInterrupt:
        print('Server stopped.')
