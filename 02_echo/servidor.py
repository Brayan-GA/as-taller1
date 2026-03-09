import socket

HOST = 'Localhost'
PORT= 9000

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT)) 
servidor.listen()

while True:
    print("El servidor 'Echo' está esperando conexiones...")

    cliente, direccion = servidor.accept()
    print("Un cliente se conectó desde la dirección: {direccion}")

    datos = cliente.recv(1024)
    if not datos:
        break

    print("Datos recibidos: ", datos)
    cliente.sendall(datos)
    cliente.close()
