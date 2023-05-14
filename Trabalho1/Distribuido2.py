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
GPIO.setmode(GPIO.BCM)

# Configuração dos pinos como saída ou entrada
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

class Cliente:
    def __init__(self, servidor, porta):
        self.servidor = servidor
        self.porta = porta
        self.cliente_socket = None

    def iniciar_cliente(self):
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente_socket.connect((self.servidor, self.porta))
        print(f"Conectado ao servidor: {self.servidor}:{self.porta}")

        thread_recebimento = threading.Thread(target=self.receber_mensagens)
        thread_recebimento.start()

        while True:
            
            #ENTRADA DE CARROS
            if GPIO.input(SENSOR_ABERTURA_CANCELA_ENTRADA) == GPIO.HIGH:
                GPIO.output(MOTOR_CANCELA_ENTRADA, GPIO.HIGH)
               ## self.enviar_mensagem(self,"Entrando carro no estacionamento")
                GPIO.input(SENSOR_DE_VAGA)
                vagas = []
                for endereco in range(8):
                    if leitura_sensor_vaga(endereco):
                        vagas.append(endereco+1)
                        def leitura_sensor_vaga(endereco):
                            GPIO.output(ENDERECO_01, (endereco & 0b001) == 0b001)
                            GPIO.output(ENDERECO_02, (endereco & 0b010) == 0b010)
                            GPIO.output(ENDERECO_03, (endereco & 0b100) == 0b100)
                            time.sleep(0.2) 
                            return GPIO.input(SENSOR_DE_VAGA)
                        

                if GPIO.wait_for_edge(SENSOR_FECHAMENTO_CANCELA_ENTRADA, GPIO.RISING):
                    GPIO.output(MOTOR_CANCELA_ENTRADA, GPIO.LOW)

            #SAÍDA DE CARROS
            if GPIO.input(SENSOR_ABERTURA_CANCELA_SAIDA) == GPIO.HIGH:
                GPIO.output(MOTOR_CANCELA_SAIDA, GPIO.HIGH)
                if GPIO.wait_for_edge(SENSOR_FECHAMENTO_CANCELA_SAIDA, GPIO.RISING):
                    GPIO.output(MOTOR_CANCELA_SAIDA, GPIO.LOW)
            


   
    
    def enviar_mensagem(self, mensagem):
        dados = {"mensagem": mensagem}
        self.cliente_socket.send(json.dumps(dados).encode())

    def receber_mensagens(self):
        while True:
            dados = self.cliente_socket.recv(1024).decode()
            mensagem = json.loads(dados)
            print(f"Mensagem recebida do servidor: {mensagem}")

    def encerrar_cliente(self):
        self.cliente_socket.close()

# Exemplo de uso
cliente = Cliente("localhost", 10231)
cliente.iniciar_cliente()

####################################Conexão com o servidor central############################################


