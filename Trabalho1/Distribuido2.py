import socket
import threading
import RPi.GPIO as GPIO
import time
import json

# Configuração dos pinos GPIO
GPIO.setmode(GPIO.BCM)

ENDERECO_01 = 22
ENDERECO_02 = 26
ENDERECO_03 = 19
SENSOR_DE_VAGA = 18
SINAL_DE_LOTADO_FECHADO = 27
SENSOR_ABERTURA_CANCELA_ENTRADA = 23
SENSOR_FECHAMENTO_CANCELA_ENTRADA = 24
MOTOR_CANCELA_ENTRADA = 10
SENSOR_ABERTURA_CANCELA_SAIDA = 25
SENSOR_FECHAMENTO_CANCELA_SAIDA = 12
MOTOR_CANCELA_SAIDA = 17

# Configuração dos pinos GPIO
GPIO.setup(ENDERECO_01, GPIO.OUT)
GPIO.setup(ENDERECO_02, GPIO.OUT)
GPIO.setup(ENDERECO_03, GPIO.OUT)
GPIO.setup(SENSOR_DE_VAGA, GPIO.IN)
GPIO.setup(SINAL_DE_LOTADO_FECHADO, GPIO.OUT)
GPIO.setup(SENSOR_ABERTURA_CANCELA_ENTRADA, GPIO.IN)
GPIO.setup(SENSOR_FECHAMENTO_CANCELA_ENTRADA, GPIO.IN)
GPIO.setup(MOTOR_CANCELA_ENTRADA, GPIO.OUT)
GPIO.setup(SENSOR_ABERTURA_CANCELA_SAIDA, GPIO.IN)
GPIO.setup(SENSOR_FECHAMENTO_CANCELA_SAIDA, GPIO.IN)
GPIO.setup(MOTOR_CANCELA_SAIDA, GPIO.OUT)

carros_andar = 0
sinal1 = 0
id_carro = 0
vagas = {'a1': 0, 'a2': 0, 'a3': 0, 'a4': 0, 'a5': 0, 'a6': 0, 'a7': 0, 'a8': 0}

class Cliente:
    def __init__(self, servidor, porta, name):
        self.servidor = servidor
        self.porta = porta
        self.name = name
        self.cliente_socket = None

    def leitura_sensor_vaga(self, endereco):
        GPIO.output(ENDERECO_01, (int(endereco) & 0b001) == 0b001)
        GPIO.output(ENDERECO_02, (int(endereco) & 0b010) == 0b010)
        GPIO.output(ENDERECO_03, (int(endereco) & 0b100) == 0b100)
        time.sleep(0.2)
        return GPIO.input(SENSOR_DE_VAGA)

    def iniciar_cliente(self):
        global sinal1, carros_andar, id_carro, vagas

        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente_socket.connect((self.servidor, self.porta))
        print(f"Conectado ao servidor: {self.servidor}:{self.porta}")

        thread_recebimento = threading.Thread(target=self.receber_mensagens)
        thread_recebimento.start()

        while True:
            # ENTRADA DE CARROS
            if GPIO.input(SENSOR_ABERTURA_CANCELA_ENTRADA) == GPIO.HIGH:
                GPIO.output(MOTOR_CANCELA_ENTRADA, GPIO.HIGH)
                envio = "O carro passou"
                vaga_ocupada = True
                self.enviar_mensagem(codigo, carros_andar, sinal1, vagas, id_carro, vg)
                                # Cria uma nova thread para enviar os números de carros no andar 1
                codigo = "entrada"
                self.enviar_mensagem(codigo, carros_andar, sinal1, vagas, id_carro, vaga_ocupada)

                print("entrando um carro")

                carros_andar += 1

                # Verifica se o sensor de fechamento da cancela de entrada foi acionado
                if GPIO.wait_for_edge(SENSOR_FECHAMENTO_CANCELA_ENTRADA, GPIO.RISING):
                    # Desativa o motor da cancela de entrada para fechar a cancela
                    GPIO.output(MOTOR_CANCELA_ENTRADA, GPIO.LOW)
                time.sleep(4)

                for i in range(8):
                    endereco = bin(i)[2:].zfill(3)  # Converte i para binário e adiciona zeros à esquerda para formar uma string de 3 dígitos
                    GPIO.output(ENDERECO_01, (int(endereco) & 0b001) == 0b001)
                    GPIO.output(ENDERECO_02, (int(endereco) & 0b010) == 0b010)
                    GPIO.output(ENDERECO_03, (int(endereco) & 0b100) == 0b100)
                    time.sleep(0.2)
                    ocupada = GPIO.input(SENSOR_DE_VAGA)
                    vg = 'a' + str(i+1)
                    print(f'vaga {vg} is {ocupada}')
                    if ocupada:
                        if vagas[vg] == 0:
                            print(f"Estacionando um carro na vaga {vg}")
                            vagas[vg] = 1
                            id_carro = 1
                            codigo = 'estaciona'
                            self.enviar_mensagem(codigo, carros_andar, sinal1, vagas, id_carro, vg)
                            id_carro = 0
                            break
                        else:
                            if vagas[vg] == 1:
                                print(f"Saindo um carro da vaga {vg}")
                                vagas[vg] = 0
                                codigo = 'saida'
                                self.enviar_mensagem(codigo, carros_andar, sinal1, vagas, id_carro, vg)
                                break

                if GPIO.wait_for_edge(SENSOR_FECHAMENTO_CANCELA_ENTRADA, GPIO.RISING):
                    GPIO.output(MOTOR_CANCELA_ENTRADA, GPIO.LOW)

            # SAÍDA DE CARROS
            if GPIO.input(SENSOR_ABERTURA_CANCELA_SAIDA) == GPIO.HIGH:
                GPIO.output(MOTOR_CANCELA_SAIDA, GPIO.HIGH)
                if GPIO.wait_for_edge(SENSOR_FECHAMENTO_CANCELA_SAIDA, GPIO.RISING):
                    GPIO.output(MOTOR_CANCELA_SAIDA, GPIO.LOW)

    def enviar_mensagem(self, codigo, carros_andar, sinal1, vagas, id_carro, vaga_ocupada):
        dados = [{
            "cod": codigo,
            "carros_andar1": carros_andar,
            "sinal1": sinal1,
            "vagas": vagas,
            "id": id_carro,
            "vaga_ocupada": vaga_ocupada
        }]

        messages = {
            "from": self.name,
            "message": dados
        }
        self.cliente_socket.send(json.dumps(messages).encode())

    def receber_mensagens(self):
        while True:
            dados = self.cliente_socket.recv(1024).decode()
            mensagem = json.loads(dados)
            print(f"Mensagem recebida do servidor: {mensagem}")

    def encerrar_cliente(self):
        self.cliente_socket.close()

# Exemplo de uso

cliente = Cliente("localhost", 10231, 'Client 1')
cliente.iniciar_cliente()





####################################Conexão com o servidor central############################################


