import json
import socket
import threading
import time

# Classe responsável pelo servidor central
class ServerCentral:
    def __init__(self, endereco, port):
        self.endereco = endereco
        self.port = port
        self.sock = None
        self.clientes = []
        self.mutex = threading.Lock()

    def iniciar(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.endereco, self.port))
        self.sock.listen(5)
        print(f"Servidor central iniciado em {self.endereco}:{self.port}")

        while True:
            cliente, endereco = self.sock.accept()
            self.mutex.acquire()
            self.clientes.append(cliente)
            self.mutex.release()
            threading.Thread(target=self.ouvir_cliente, args=(cliente,)).start()

    def enviar_mensagem(self, cliente, mensagem):
        try:
            cliente.sendall(mensagem.encode())
        except:
            cliente.close()
            self.mutex.acquire()
            self.clientes.remove(cliente)
            self.mutex.release()

    def ouvir_cliente(self, cliente):
        while True:
            try:
                data = cliente.recv(1024)
                if data:
                    mensagem = data.decode()
                    self.processar_mensagem(mensagem)
                else:
                    cliente.close()
                    self.mutex.acquire()
                    self.clientes.remove(cliente)
                    self.mutex.release()
                    break
            except:
                cliente.close()
                self.mutex.acquire()
                self.clientes.remove(cliente)
                self.mutex.release()
                break

    def processar_mensagem(self, mensagem):
        # Processar a mensagem recebida do servidor distribuído
        pass

    def enviar_comando_para_servidores(self, comando):
        mensagem = json.dumps(comando)

        self.mutex.acquire()
        for cliente in self.clientes:
            threading.Thread(target=self.enviar_mensagem, args=(cliente, mensagem)).start()
        self.mutex.release()

# Configurações do servidor central
endereco_central = '192.168.0.100'
port_central = 10963

# Criar uma instância do servidor central
servidor_central = ServerCentral(endereco_central, port_central)

# Iniciar o servidor central
servidor_central.iniciar()
