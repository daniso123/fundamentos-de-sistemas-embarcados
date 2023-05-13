import RPi.GPIO as GPIO
import socket
import threading
import json

class ServidorCentral:
    def __init__(self, endereco, porta):
        self.endereco = endereco
        self.porta = porta
        self.servidor_socket = None
        self.clientes = []

         # Variáveis de controle de estacionamento
        self.num_carros_andar = [0, 0, 0]  # Número de carros em cada andar
        self.num_total_carros = 0
        self.num_carros_total = 0  # Número total de carros no estacionamento
        self.num_vagas_disponiveis = [8,8 , 8]  # Número de vagas disponíveis em cada andar
        self.valor_total_pago = 0.0  # Valor total pago

        

    def iniciar_servidor(self):
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor_socket.bind((self.endereco, self.porta))
        self.servidor_socket.listen(5)
        print(f"Servidor central iniciado em {self.endereco}:{self.porta}")

        while True:
            cliente_socket, cliente_endereco = self.servidor_socket.accept()
            cliente_thread = threading.Thread(target=self.lidar_conexao, args=(cliente_socket,))
            cliente_thread.start()
            self.clientes.append((cliente_socket, cliente_endereco))
            print(f"Novo cliente conectado: {cliente_endereco}")

    def lidar_conexao(self, cliente_socket):
        while True:
            try:
                dados = cliente_socket.recv(1024).decode()
                mensagem = json.loads(dados)
                print(f"Mensagem recebida do cliente: {mensagem}")
            

                if "mensagem" in mensagem:
                    if mensagem["mensagem"] == "Entrando carro no estacionamento":
                        self.num_total_carros= self.num_total_carros + 1

                        # Atualiza as informações recebidas do cliente
                        if 'num_carros_andar' in mensagem:
                            self.num_carros_andar = mensagem['num_carros_andar']
                            self.num_carros_andar= self.num_carros_andar+1
                        if 'num_vagas_disponiveis' in mensagem:
                            self.num_vagas_disponiveis = mensagem['num_vagas_disponiveis']
                            GPIO.input(SENSOR_DE_VAGA)
                            vagas = []
                            for endereco in range(8):
                                if leitura_sensor_vaga(endereco):
                                    vagas.append(endereco+1)

                        if 'valor_total_pago' in mensagem:
                            self.valor_total_pago = mensagem['valor_total_pago']

                # Cálculo do valor total pago
                valor_pago = self.calcular_valor_pago()
                self.enviar_mensagem_cliente(cliente_socket, {'valor_pago': valor_pago})

            except ConnectionResetError:
                self.clientes.remove(cliente_socket)
                print("Cliente desconectado")
                break

        cliente_socket.close()

    def leitura_sensor_vaga(endereco):
        GPIO.output(ENDERECO_01, (endereco & 0b001) == 0b001)
        GPIO.output(ENDERECO_02, (endereco & 0b010) == 0b010)
        GPIO.output(ENDERECO_03, (endereco & 0b100) == 0b100)
        time.sleep(0.2) 
        return GPIO.input(SENSOR_DE_VAGA)

    def calcular_valor_pago(self):
        minutos_estacionados = sum(self.num_carros_andar)  # Considera que cada carro estacionado corresponde a 1 minuto
        valor_pago = minutos_estacionados * 0.15  # Taxa de R$ 0,15 (quinze centavos) por minuto
        return valor_pago

    def enviar_mensagem_cliente(self, cliente_socket, mensagem):
        cliente_socket.send(json.dumps(mensagem).encode())

    def enviar_mensagem_todos_clientes(self, mensagem):
        for cliente_socket, _ in self.clientes:
            cliente_socket.send(json.dumps(mensagem).encode())

    def encerrar_servidor(self):
        self.servidor_socket.close()

# Exemplo de uso
servidor = ServidorCentral("localhost", 10231)
servidor.iniciar_servidor()





