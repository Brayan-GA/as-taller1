import socket
import threading

HOST = "localhost"
PORT = 65435
EXIT_COMMANDS = {"exit", "quit", "salir"}

def send(conn, msg):
    conn.sendall(f"{msg}\n".encode("utf-8"))

def receive(file):
    while True:
        line = file.readline()
        if not line:
            print("\nServidor desconectado.")
            break
        print(f"\n{line.strip()}\nComando> ", end="", flush=True)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            print("No se pudo conectar al servidor.")
            return

        file = s.makefile("r", encoding="utf-8", newline="\n")
        threading.Thread(target=receive, args=(file,), daemon=True).start()

        # Registro de usuario
        while True:
            name = input("Tu nombre> ").strip()
            if name:
                send(s, f"REGISTER {name}")
                break

        # Bucle de comandos
        while True:
            try:
                cmd = input("Comando> ").strip()
            except EOFError:
                cmd = "EXIT"
            if not cmd:
                continue
            send(s, cmd)
            if cmd.lower() in EXIT_COMMANDS:
                break

if __name__ == "__main__":
    main()