import random

# Lista de clientes (zumbis)
clientes = [
    {'nome': 'Máquina 1', 'tipo': 'Máquina'},
    {'nome': 'Câmera 1', 'tipo': 'Câmera'},
    {'nome': 'Máquina 2', 'tipo': 'Máquina'},
    {'nome': 'Câmera 2', 'tipo': 'Câmera'},
]

def verificar_clientes():
    """Verifica o status dos clientes e retorna uma lista de dicionários com os dados."""
    status_clientes = []
    for cliente in clientes:
        status = verificar_status(cliente['nome'])
        status_clientes.append({
            'nome': cliente['nome'],
            'tipo': cliente['tipo'],
            'status': status,
        })
    return status_clientes

def verificar_status(nome):
    """Simula a verificação do status do cliente (online/offline)."""
    return 'Ativa' if random.choice([True, False]) else 'Inativa'

# Para testes, você pode testar a função diretamente
if __name__ == "__main__":
    print(verificar_clientes())