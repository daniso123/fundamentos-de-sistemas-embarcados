import json
import socket
import threading
import time


class ServerCentral:
    def __init__(self, endereco, port):
        self.endereco = endereco
        self.port = port
        self.sock = None
        self.clientes = []
        self.mutex = threading.Lock()
        self.andar1_vagas_disponiveis = 0
        self.andar2_vagas_disponiveis = 0
        self.andar1_carros_estacionados = 0
        self.andar2_carros_estacionados = 0
        self.total_carros = 0
        self.valor_total_pago = 0
        self.sinal_lotado = False
        self.estacionamento_fechado = False

    def iniciar(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.endereco, self.port))
        self.sock.listen(5)
        #print(f"Servidor central iniciado em {self.endereco}:{self.port}")
        print("Servidor central iniciado em {}:{}".format(self.endereco, self.port))

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
        try:
            comando = json.loads(mensagem)
            if 'andar' in comando and 'vagas_disponiveis' in comando:
                if comando['andar'] == 1:
                    self.andar1_vagas_disponiveis = comando['vagas_disponiveis']
                elif comando['andar'] == 2:
                    self.andar2_vagas_disponiveis = comando['vagas_disponiveis']
            elif 'andar' in comando and 'carros_estacionados' in comando:
                if comando['andar'] == 1:
                    self.andar1_carros_estacionados = comando['carros_estacionados']
                elif comando['andar'] == 2:
                    self.andar2_carros_estacionados = comando['carros_estacionados']
            elif 'total_carros' in comando:
                self.total_carros = comando['total_carros']
            elif 'valor_pago' in comando:
                self.valor_total_pago = comando['valor_pago']
        except:
            pass

    def enviar_comando_para_servidores(self, comando):
        mensagem = json.dumps(comando)

        self.mutex.acquire()
        for cliente in self.clientes:
            threading.Thread(target=self.enviar_mensagem, args=(cliente, mensagem)).start()
        self.mutex.release()

    def calcular_valor_pago(self, minutos):
        return minutos * 0.15

    def fechar_estacionamento_manual(self, fechar):
            self.estacionamento_fechado = fechar
            comando = {'estacionamento_fechado': self.estacionamento_fechado}
            self.enviar_comando_para_servidores(comando)

    def bloquear_segundo_andar(self, bloquear):
            self.sinal_lotado = bloquear
            comando = {'sinal_lotado': self.sinal_lotado}
            self.enviar_comando_para_servidores(comando)

    def atualizar_interface(self):
            while True:
                #Atualizar informações na interface (exemplo: imprimir no console)
                print("--------- Estado Atual ---------")
                print(f"Andar 1 - Vagas Disponíveis: {self.andar1_vagas_disponiveis}")
                print(f"Andar 1 - Carros Estacionados: {self.andar1_carros_estacionados}")
                print(f"Andar 2 - Vagas Disponíveis: {self.andar2_vagas_disponiveis}")
                print(f"Andar 2 - Carros Estacionados: {self.andar2_carros_estacionados}")
                print(f"Total de Carros no Estacionamento: {self.total_carros}")
                print(f"Valor Total Pago: R$ {self.valor_total_pago}")
                print(f"Estacionamento Fechado: {self.estacionamento_fechado}")
                print(f"Bloqueio do 2º Andar: {self.sinal_lotado}")
                print("--------------------------------")

                time.sleep(5)  # Atualizar a cada 5 segundos

    def run(self):
        threading.Thread(target=self.iniciar).start()
        threading.Thread(target=self.atualizar_interface).start()

if __name__ == "__main__":
    servidor = ServerCentral('localhost', 8000)
    servidor.run()

