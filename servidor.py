import socket 
import threading

clientes_status = {}

def servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=gerenciar_cliente, args=(client_socket,)).start()

def gerenciar_cliente(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            nome, status = data.split(',')
            clientes_status[nome] = status
        except ConnectionResetError:
            break
    client_socket.close()