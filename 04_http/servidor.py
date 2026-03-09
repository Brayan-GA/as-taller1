import socket
import http.server

HOST = 'localhost'
PORT = 9000

class Servidor(http.server.SimpleHTTPRequestHandler):
    pass

servidor = http.server.HTTPServer((HOST, PORT), Servidor)
servidor.serve_forever()