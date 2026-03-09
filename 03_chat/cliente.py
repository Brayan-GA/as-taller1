import socket
import threading

HOST = 'localhost'
PORT = 9000

def recibir_mensajes(cliente):
    while True:
            mensaje = cliente.recv(1024).decode()
            print (mensaje)


nombre = input("Ingrese su nombre: ")
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))
cliente.sendall(nombre.encode())

hilo_receptor = threading.Thread(target=recibir_mensaje)
hilo_receptor.start()

while True:
    mensaje = input("Mensaje: ")
    cliente.sendall(mensaje.encode())
