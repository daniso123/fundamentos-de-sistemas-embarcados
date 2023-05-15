
import socket
import threading
from datetime import datetime
import json

carros_andar1 = 0; sinal1 = 0
vagas1 = {'a1': 0, 'a2': 0, 'a3': 0, 'a4': 0, 'a5': 0, 'a6': 0, 'a7': 0, 'a8': 0}
carros_andar2= 0; sinal2= 0
vagas2 = {'b1': 0, 'b2': 0, 'b3': 0, 'b4': 0, 'b5': 0, 'b6': 0, 'b7': 0, 'b8': 0}
total_carros = 0
id_carro = 0


class Carro:
    def __init__(self, id_carro, vaga, data_hora_entrada):
        self.id_carro = id_carro
        self.vaga = vaga
        self.data_hora_entrada = data_hora_entrada

lista_carros = []

class ServidorCentral:
    def __init__(self, endereco, porta):
        self.endereco = endereco
        self.porta = porta
        self.servidor_socket = None
        self.clientes = []

         # Variáveis de controle de estacionamento
        self.num_carros_andar = [0, 0, 0]  # Número de carros em cada andar
        self.num_total_carros = 0
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
            

                if mensagem == "ping":
                    continue
                # print(f"Received message from {message['from']}: {message['message']}")
                global carros_andar1, sinal1, vagas1, carros_andar2, sinal2, vagas2, total_carros, id_carro
                # Tratamento de mensagem adicionado
                if mensagem['from'] == 'Client 1':
                    
                    carros_andar1 = mensagem['message'][0]['carros_andar1']
                    sinal1 = mensagem['message'][0]['sinal1']
                    vagas1 = mensagem['message'][0]['vagas'] 
                    id_carro = id_carro + mensagem['message'][0]['id']
                    vaga_ocupada = mensagem['message'][0]['vaga_ocupada']
                    if (carros_andar1 + carros_andar2 >= 16 and sinal1 == 0) or (carros_andar1 >= 8 and sinal2 == 1):
                        self.send_message("Fechar andar 1")
                    # if (carros_andar1 + carros_andar2 < 16 ) or (carros_andar1 < 8 and sinal2 == 1):
                    #     self.send_message("Abrir andar 1")
                        
                    if mensagem['message'][0]['cod'] == 'entrada':
                        total_carros = total_carros + 1
                    elif mensagem['message'][0]['cod'] == 'estaciona':
                        print(f'Carro andar 1 com ID {id_carro} estacionado na vaga {vaga_ocupada}')
                        lista_carros.append(Carro(id_carro, vaga_ocupada, datetime.now()))
                    elif mensagem['message'][0]['cod'] == 'saida':
                        for carro in lista_carros:
                            if carro.vaga == vaga_ocupada:
                                print(f"O carro {carro.id_carro} está na vaga {carro.vaga}")
                                lista_carros.remove(carro)
                                

                    elif mensagem['from'] == 'Client 2':
                        if mensagem['message'] == 'entrando andar2':
                            self.send_message('entrando andar2')
                        print('entrando andar2')
                    elif mensagem['message'] == 'saindo andar2':
                            self.send_message('saindo andar2')
                    else:
                        carros_andar2 = mensagem['message'][0].get('carros_andar2', 0)
                        # carros_andar2 = mensagem['message'][0]['carros_andar2']
                        sinal2 = mensagem['message'][0]['sinal2']
                        vagas2 = mensagem['message'][0]['vagas'] 
                        id_carro = id_carro + mensagem['message'][0]['id']
                        vaga_ocupada = mensagem['message'][0]['vaga_ocupada']
                        if carros_andar2 >= 8 and sinal2 == 0:
                            self.send_message("Fechar andar 2")
                        
                        # if carros_andar2 < 8:
                        #     self.send_message("Abrir andar 2")    
                            
                        elif mensagem['message'][0]['cod'] == 'estaciona':
                            print(f'Carro andar 2 com ID {id_carro} estacionado na vaga {vaga_ocupada}')
                            lista_carros.append(Carro(id_carro, vaga_ocupada, datetime.now()))
                        elif mensagem['message'][0]['cod'] == 'saida':
                            for carro in lista_carros:
                                if carro.vaga == vaga_ocupada:
                                    print(f"O carro {carro.id_carro} está na vaga {carro.vaga}")
                                    lista_carros.remove(carro)
                                    data_dif = datetime.now() - carro.data_hora_entrada
                            

                     

                # Cálculo do valor total pago
                valor_pago = self.calcular_valor_pago()
                self.enviar_mensagem_cliente(cliente_socket, {'valor_pago': valor_pago})
                self.enviar_mensagem_cliente(cliente_socket, {'vagas_disponiveis': self.num_vagas_disponiveis})


            except ConnectionResetError:
                self.clientes.remove(cliente_socket)
                print("Cliente desconectado")
                break

        cliente_socket.close()



    def calcular_valor_pago(self):
        minutos_estacionados = sum(self.num_carros_andar)  # Considera que cada carro estacionado corresponde a 1 minuto
        valor_pago = minutos_estacionados * 0.15  # Taxa de R$ 0,15 (quinze centavos) por minuto
        return valor_pago

    def enviar_mensagem_cliente(self, cliente_socket, mensagem):
        cliente_socket.send(json.dumps(mensagem).encode())

    def send_message(self, message):
      message_dict = {"from": "Server", "message": message}
      self.broadcast(message_dict, None)

    def enviar_mensagem_todos_clientes(self, mensagem):
        for cliente_socket, _ in self.clientes:
            cliente_socket.send(json.dumps(mensagem).encode())

    def encerrar_servidor(self):
        self.servidor_socket.close()

# Exemplo de uso
servidor = ServidorCentral("localhost", 10231)
servidor.iniciar_servidor()





