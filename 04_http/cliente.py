import socket
import http.client

HOST = 'localhost'
PORT = 9000

cliente = http.client.HTTPConnection(HOST, PORT)
cliente.request("GET", "/")

respuesta = cliente.getresponse()
datos = respuesta.read().decode()

print(datos)

cliente.close()