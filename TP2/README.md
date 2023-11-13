## Ejecución

# Lado del Servidor:

Ejecuta el servidor en la terminal:

# Ejemplo para IPv4:

python3 TP2.py -i 127.0.0.1 -p 4200

# Ejemplo para IPv6:

python3 TP2.py -i ::1 -p 8000

Los argumentos son opcionales, si no se escribe ninguno se ejecutara en el :: con puerto 8080

# Lado del Cliente:

Utilizando curl para enviar una solicitud POST con una imagen al servidor:

curl -X POST -H "Content-Type: image/jpeg" --data-binary @input_image.jpg http://127.0.0.1:4200 --output received_image.jpg

En este caso la imagen se guardara en el directorio.




