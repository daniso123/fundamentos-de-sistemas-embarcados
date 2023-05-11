import socket
import threading
import time
import RPi.GPIO as GPIO
import json

class ServerDistribuido:
    def __init__(self, servidor_central_ip, servidor_central_porta, andar):
        self.servidor_central_ip = servidor_central_ip
        self.servidor_central_porta = servidor_central_porta
        self.andar = andar
        self.cancela_entrada_aberta = False
        self.cancela_saida_aberta = False

        if andar == 1:
            self.GPIO_CANCELA_ENTRADA_SENSOR_ABERTURA = 23
            self.GPIO_CANCELA_ENTRADA_SENSOR_FECHAMENTO = 24
            self.GPIO_CANCELA_ENTRADA_MOTOR = 10
            self.GPIO_CANCELA_SAIDA_SENSOR_ABERTURA = 25
            self.GPIO_CANCELA_SAIDA_SENSOR_FECHAMENTO = 12
            self.GPIO_CANCELA_SAIDA_MOTOR = 17

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
        # Lógica para ler periodicamente a ocupação das vagas e enviar as mudanças de estado ao servidor central
        threading.Timer(5, self.ler_ocupacao_vagas).start()  # Agendar a próxima execução após 5 segundos

        # Verificar a ocupação de cada estacionamento
        for estacionamento in self.estacionamentos:
            andar = estacionamento.andar
            vagas_ocupadas = estacionamento.vagas_ocupadas()

            # Lógica para enviar as mudanças de estado ao servidor central
            mensagem = {
                "acao": "ocupacao_vagas",
                "andar": andar,
                "vagas_ocupadas": vagas_ocupadas
            }
            mensagem_json = json.dumps(mensagem)
            # Estabelecer a conexão com o servidor central
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.servidor_central_ip, self.servidor_central_porta))
            # Enviar a mensagem de ocupação de vagas
            sock.sendall(mensagem_json.encode())
            # Fechar a conexão
            sock.close()


    def abrir_cancela_entrada(self):
        # Lógica para abrir a cancela de entrada quando um carro estiver na espera
        GPIO.output(self.GPIO_CANCELA_ENTRADA_MOTOR, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(self.GPIO_CANCELA_ENTRADA_MOTOR, GPIO.LOW)

    def fechar_cancela_entrada(self):
        # Lógica para fechar a cancela de entrada quando não houver carro na espera
        GPIO.output(self.GPIO_CANCELA_ENTRADA_MOTOR, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(self.GPIO_CANCELA_ENTRADA_MOTOR, GPIO.LOW)

    def abrir_cancela_saida(self):
        # Lógica para abrir a cancela de saída quando um carro estiver saindo
        GPIO.output(self.GPIO_CANCELA_SAIDA_MOTOR, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(self.GPIO_CANCELA_SAIDA_MOTOR, GPIO.LOW)

    def fechar_cancela_saida(self):
        # Lógica para fechar a cancela de saída quando não houver carro saindo
        GPIO.output(self.GPIO_CANCELA_SAIDA_MOTOR, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(self.GPIO_CANCELA_SAIDA_MOTOR, GPIO.LOW)

    def enviar_mensagem_registro_entrada(self, vaga, data_hora):
    # Lógica para enviar uma mensagem ao servidor central informando o registro de entrada de um carro na vaga especificada
        mensagem = {
            "acao": "registro_entrada",
            "andar": self.andar,
            "vaga": vaga,
            "data_hora": data_hora
        }
        mensagem_json = json.dumps(mensagem)
    
    # Código para enviar a mensagem ao servidor central utilizando sockets

def enviar_mensagem_registro_saida(self, vaga,data_hora):
    # Lógica para enviar uma mensagem ao servidor central informando o registro de saída de um carro da vaga especificada
    mensagem = {
        "acao": "registro_saida",
        "andar": self.andar,
        "vaga": vaga,
        "data_hora": data_hora
    }
    mensagem_json = json.dumps(mensagem)
    # Estabelecer a conexão com o servidor central
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((self.servidor_central_ip, self.servidor_central_porta))
    # Enviar a mensagem de registro
    sock.sendall(mensagem_json.encode())
    # Aguardar a confirmação do servidor central
    resposta = sock.recv(1024)  # Tamanho máximo da resposta definido como 1024 bytes

    if resposta:
    # Fazer algo com a resposta recebida do servidor central
        print("Resposta do servidor central:", resposta.decode())
    else:
        print("Nenhuma resposta do servidor central.")
    # Fechar a conexão
    sock.close()
    
    # Código para enviar a mensagem ao servidor central utilizando sockets

def acionar_sinal_lotado(self):
    lotado = True
    for estacionamento in self.estacionamentos:
        if not estacionamento.cheio():
            lotado = False
            break
    if lotado:
        # Lógica para acionar o sinal de lotado
        print("Todas as vagas estão ocupadas. Acionando sinal de lotado.")


def detectar_passagem_carro(self, andar, vaga):
    estacionamento = self.encontrar_estacionamento(andar)
    if estacionamento:
        if not estacionamento.cheio():
            estacionamento.registrar_entrada(vaga)
        else:
            # Lógica para informar que não há vagas disponíveis no estacionamento
            print("Não há vagas disponíveis no estacionamento.")
    else:
        # Lógica para informar que o estacionamento não foi encontrado
        print("Estacionamento não encontrado.")

                
def iniciar_servidor(self):
    # Lógica para iniciar o servidor distribuído e aguardar conexões
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', self.servidor_central_porta)
    sock.bind(server_address)
    sock.listen(1)
    print(f"Servidor distribuído do andar {self.andar} iniciado na porta {self.servidor_central_porta}.")
    
    while True:
        # Aguardar uma conexão
        print("Aguardando conexão...")
        client_socket, client_address = sock.accept()
        print(f"Conexão estabelecida com {client_address}")
        
        # Iniciar uma nova thread para lidar com a conexão
        thread = threading.Thread(target=self.lidar_com_conexao, args=(client_socket,))
        thread.start()
        
def lidar_com_conexao(self, sock):
    # Lógica para lidar com uma conexão de cliente
    while True:
        # Receber os dados enviados pelo cliente
        data = sock.recv(1024)
        
        if not data:
            # Se não houver dados, encerrar a conexão
            print("Conexão encerrada pelo cliente.")
            break
        
        # Decodificar os dados recebidos
        mensagem_json = data.decode()
        mensagem = json.loads(mensagem_json)
        
        # Verificar a ação solicitada na mensagem
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
            
    # Fechar o socket da conexão
    sock.close()
    
# Exemplo de uso
servidor = ServerDistribuido("127.0.0.1", 5000, 1)
servidor.iniciar_servidor()
