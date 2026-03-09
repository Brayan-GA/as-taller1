import socket
import threading

HOST = 'localhost'
PORT = 9000

clientes = []

def atender_cliente(cliente, nombre):
    while True:
        try:
            mensaje = cliente.recv(1024)
            if not mensaje:
                break
            print(f"{nombre}: {mensaje.decode()}")
            broadcast(mensaje.decode(), cliente)
        except ConnectionResetError:
            clientes.remove(cliente)
            cliente.close()
            break

def broadcast(mensaje, emisor):
    for cliente in clientes:
        if cliente != emisor:
            cliente.send(mensaje.encode())  


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()
print("El servidor 'chat' está esperando conexiones...")

while True:
    cliente, direccion = servidor.accept()
    print(f"Un cliente se conectó desde la dirección IP: {direccion}")     
    nombre = cliente.recv(1024).decode()
    clientes.append(cliente)
    broadcast(f"{nombre} se ha unido al chat.", cliente)
    hilo_cliente = threading.Thread(target=atender_cliente, args=(cliente, nombre))
    hilo_cliente.start()
