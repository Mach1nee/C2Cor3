import socket
import time
import random

def verificar_status():
    """Simula a verificação do status do cliente (online/offline)."""
    return 'Ativa' if random.choice([True, False]) else 'Inativa'

def main():
    server_address = ('localhost', 12345)  # Altere para o IP do servidor se necessário

    while True:
        # Cria o socket do cliente
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            # Conecta ao servidor
            client_socket.connect(server_address)
            nome = "Máquina 1"  # Nome do cliente; pode ser alterado conforme necessário
            status = verificar_status()
            message = f"{nome},{status}"
            client_socket.sendall(message.encode())
            print(f"Enviado: {message}")
        except Exception as e:
            print(f"Erro ao conectar ou enviar: {e}")
        finally:
            client_socket.close()

        time.sleep(5)  # Espera 5 segundos antes de enviar novamente

if __name__ == "__main__":
    main()