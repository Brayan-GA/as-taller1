import socket

HOST = 'Localhost'
PORT= 9000

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT)) 
servidor.listen()
print("El servidor está a la espera de conexiones...")

cliente, direccion = servidor.accept()
print("Un cliente se conectó desde: {direccion}")

datos = cliente.recv(1024)
cliente.sendall(b"Hola! "+ datos) # Debe ser binario, no string
cliente.close()
