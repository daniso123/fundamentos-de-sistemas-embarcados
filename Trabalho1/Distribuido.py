import socket
import threading
import time
import RPi.GPIO as GPIO
import json

class ServerDistribuido:
    def __init__(self, servidor_central_ip, servidor_central_porta, andar):
        GPIO.setmode(GPIO.BOARD)
        self.servidor_central_ip = servidor_central_ip
        self.servidor_central_porta = servidor_central_porta
        self.andar = andar
        self.cancela_entrada_aberta = False
        self.cancela_saida_aberta = False

        if andar == 1:
            self.GPIO_CANCELA_ENTRADA_SENSOR_ABERTURA = 10
            self.GPIO_CANCELA_ENTRADA_SENSOR_FECHAMENTO = 22
            self.GPIO_CANCELA_ENTRADA_MOTOR = 5
            self.GPIO_CANCELA_SAIDA_SENSOR_ABERTURA = 27
            self.GPIO_CANCELA_SAIDA_SENSOR_FECHAMENTO = 17
            self.GPIO_CANCELA_SAIDA_MOTOR = 0

            GPIO.setup(self.GPIO_CANCELA_ENTRADA_SENSOR_ABERTURA, GPIO.IN)
            GPIO.setup(self.GPIO_CANCELA_ENTRADA_SENSOR_FECHAMENTO, GPIO.IN)
            GPIO.setup(self.GPIO_CANCELA_ENTRADA_MOTOR, GPIO.OUT)
            GPIO.setup(self.GPIO_CANCELA_SAIDA_SENSOR_ABERTURA, GPIO.IN)
            GPIO.setup(self.GPIO_CANCELA_SAIDA_SENSOR_FECHAMENTO, GPIO.IN)
            GPIO.setup(self.GPIO_CANCELA_SAIDA_MOTOR, GPIO.OUT)
        elif andar == 2:
            self.GPIO_SENSOR_PASSAGEM_1 = 16
            self.GPIO_SENSOR_PASSAGEM_2 = 21

            GPIO.setup(self.GPIO_SENSOR_PASSAGEM_1, GPIO.IN)
            GPIO.setup(self.GPIO_SENSOR_PASSAGEM_2, GPIO.IN)

    def ler_ocupacao_vagas(self):

        threading.Timer(5, self.ler_ocupacao_vagas).start()


        for estacionamento in self.estacionamentos:
            andar = estacionamento.andar
            vagas_ocupadas = estacionamento.vagas_ocupadas()

            mensagem = {
                "acao": "ocupacao_vagas",
                "andar": andar,
                "vagas_ocupadas": vagas_ocupadas
            }
            mensagem_json = json.dumps(mensagem)

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.servidor_central_ip, self.servidor_central_porta))

            sock.sendall(mensagem_json.encode())

            sock.close()


    def abrir_cancela_entrada(self):

        GPIO.output(self.GPIO_CANCELA_ENTRADA_MOTOR, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(self.GPIO_CANCELA_ENTRADA_MOTOR, GPIO.LOW)

    def fechar_cancela_entrada(self):

        GPIO.output(self.GPIO_CANCELA_ENTRADA_MOTOR, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(self.GPIO_CANCELA_ENTRADA_MOTOR, GPIO.LOW)

    def abrir_cancela_saida(self):

        GPIO.output(self.GPIO_CANCELA_SAIDA_MOTOR, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(self.GPIO_CANCELA_SAIDA_MOTOR, GPIO.LOW)

    def fechar_cancela_saida(self):

        GPIO.output(self.GPIO_CANCELA_SAIDA_MOTOR, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(self.GPIO_CANCELA_SAIDA_MOTOR, GPIO.LOW)

    def enviar_mensagem_registro_entrada(self, vaga, data_hora):

        mensagem = {
            "acao": "registro_entrada",
            "andar": self.andar,
            "vaga": vaga,
            "data_hora": data_hora
        }
        mensagem_json = json.dumps(mensagem)



def enviar_mensagem_registro_saida(self, vaga,data_hora):

    mensagem = {
        "acao": "registro_saida",
        "andar": self.andar,
        "vaga": vaga,
        "data_hora": data_hora
    }
    mensagem_json = json.dumps(mensagem)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((self.servidor_central_ip, self.servidor_central_porta))

    sock.sendall(mensagem_json.encode())

    resposta = sock.recv(1024)

    if resposta:

        print("Resposta do servidor central:", resposta.decode())
    else:
        print("Nenhuma resposta do servidor central.")

    sock.close()
    


def acionar_sinal_lotado(self):
    lotado = True
    for estacionamento in self.estacionamentos:
        if not estacionamento.cheio():
            lotado = False
            break
    if lotado:

        print("Todas as vagas estão ocupadas. Acionando sinal de lotado.")


def detectar_passagem_carro(self, andar, vaga):
    estacionamento = self.encontrar_estacionamento(andar)
    if estacionamento:
        if not estacionamento.cheio():
            estacionamento.registrar_entrada(vaga)
        else:

            print("Não há vagas disponíveis no estacionamento.")
    else:

        print("Estacionamento não encontrado.")

                
def iniciar_servidor(self):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', self.servidor_central_porta)
    sock.bind(server_address)
    sock.listen(1)
    print(f"Servidor distribuído do andar {self.andar} iniciado na porta {self.servidor_central_porta}.")
    
    while True:

        print("Aguardando conexão...")
        client_socket, client_address = sock.accept()
        print(f"Conexão estabelecida com {client_address}")
        

        thread = threading.Thread(target=self.lidar_com_conexao, args=(client_socket,))
        thread.start()
        
def lidar_com_conexao(self, sock):

    while True:

        data = sock.recv(1024)
        
        if not data:

            print("Conexão encerrada pelo cliente.")
            break
        

        mensagem_json = data.decode()
        mensagem = json.loads(mensagem_json)
        

        acao = mensagem.get("acao")
        
        if acao == "abrir_cancela_entrada":
            self.abrir_cancela_entrada()
        elif acao == "fechar_cancela_entrada":
            self.fechar_cancela_entrada()
        elif acao == "abrir_cancela_saida":
            self.abrir_cancela_saida()
        elif acao == "fechar_cancela_saida":
            self.fechar_cancela_saida()
        elif acao == "enviar_mensagem_registro_entrada":
            vaga = mensagem.get("vaga")
            data_hora = mensagem.get("data_hora")
            self.enviar_mensagem_registro_entrada(vaga, data_hora)
        elif acao == "enviar_mensagem_registro_saida":
            vaga = mensagem.get("vaga")
            data_hora = mensagem.get("data_hora")
            self.enviar_mensagem_registro_saida(vaga, data_hora)
            

    sock.close()
    

servidor = ServerDistribuido("164.41.98.15", 10231, 1)
servidor.iniciar_servidor()
