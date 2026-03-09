import socket
import threading

HOST = "localhost"
PORT = 65435
EXIT_COMMANDS = {"EXIT", "SALIR", "QUIT"}

clients = {}
lock = threading.Lock()

def send(conn, msg):
    conn.sendall(f"{msg}\n".encode("utf-8"))

def broadcast(msg, exclude=None):
    with lock:
        for c in clients.keys():
            if c != exclude:
                try:
                    send(c, msg)
                except:
                    pass

def handle_client(conn, addr):
    send(conn, "Bienvenido! Regístrate con: REGISTER <nombre>")
    name = None

    try:
        file = conn.makefile("r", encoding="utf-8", newline="\n")
        while True:
            line = file.readline()
            if not line:
                break
            parts = line.strip().split(maxsplit=1)
            if not name:
                if len(parts) == 2 and parts[0].upper() == "REGISTER":
                    name_candidate = parts[1].strip()
                    with lock:
                        if name_candidate not in clients.values():
                            clients[conn] = name_candidate
                            name = name_candidate
                            send(conn, f"Registro exitoso como {name}.")
                            send(conn, "Comandos: USERS | ALL <mensaje> | MSG <usuario> <mensaje> | EXIT")
                            broadcast(f"[SISTEMA] {name} se ha conectado.", exclude=conn)
                            break
                        else:
                            send(conn, "Nombre en uso, intenta otro.")
                else:
                    send(conn, "Debes registrarte primero. Uso: REGISTER <nombre>")
        # Bucle de comandos
        while True:
            line = file.readline()
            if not line:
                break
            text = line.strip()
            if not text:
                continue
            cmd_parts = text.split(maxsplit=2)
            cmd = cmd_parts[0].upper()
            if cmd in EXIT_COMMANDS:
                send(conn, "Desconectado.")
                break
            elif cmd == "USERS":
                with lock:
                    user_list = ", ".join(clients.values()) or "No hay usuarios conectados."
                send(conn, f"Usuarios conectados: {user_list}")
            elif cmd == "ALL" and len(cmd_parts) > 1:
                msg = text.split(maxsplit=1)[1]
                broadcast(f"[GLOBAL] {name}: {msg}", exclude=conn)
                send(conn, "Mensaje global enviado.")
            elif cmd == "MSG" and len(cmd_parts) == 3:
                target_name, msg = cmd_parts[1], cmd_parts[2]
                with lock:
                    target_conn = next((c for c, n in clients.items() if n == target_name), None)
                if target_conn:
                    send(target_conn, f"[PRIVADO] {name}: {msg}")
                    send(conn, f"Mensaje privado enviado a {target_name}.")
                else:
                    send(conn, f"Usuario {target_name} no encontrado.")
            else:
                send(conn, "Comando no reconocido.")
    finally:
        with lock:
            if conn in clients:
                disconnected_name = clients.pop(conn)
                broadcast(f"[SISTEMA] {disconnected_name} se ha desconectado.")
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor escuchando en {HOST}:{PORT}")
        try:
            while True:
                conn, addr = s.accept()
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
        except KeyboardInterrupt:
            print("\nServidor detenido.")

if __name__ == "__main__":
    main()