import socket

HOST = 'Localhost'
PORT= 9000

mensaje = input("Degite su mensaje: ")
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT)) 

cliente.sendall(mensaje.encode())
print(f"Mensaje enviado: '{mensaje}'")

respuesta = cliente.recv(1024)
print(f"Respuesta del 'Echo': {respuesta.decode()}")

cliente.close()