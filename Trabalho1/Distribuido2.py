import sys
import json
import socket
import threading


from time import sleep



#print("Config:")
#print(sys.argv[1])

dicionario_configuracao = []

with open(sys.argv[1]) as arquivo_entrada:
    dicionario_configuracao = json.load(arquivo_entrada)


#mensagens no formato json
fila_mensagens_para_envio = []

servidor = '164.41.98.15'
port = 10231

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
clientSocket.connect((servidor, port));


def metodo_recebimento_mensagens(fila_mensagens):
    while True:
        dataFromServer = clientSocket.recv(1024)
        print(dataFromServer.decode())
        dicionario_resposta = json.loads(dataFromServer.decode())


        # Direcionamento para cada função dependendo do requerimento

        if "ligar_desligar_aparelho" in dicionario_resposta.keys():
            print("Key ligar_desligar_aparelho encontrada")
            #interruptor_aparelhos(dicionario_resposta["ligar_desligar_aparelho"][0],dicionario_resposta["ligar_desligar_aparelho"][1])


        #if "Temperatura" in dicionario_resposta.keys():
            #fila_mensagens.append(leitor_temperatura())

        sleep(0.5)

def metodo_envio_mensagens(fila_mensagens:dict):
    while True:
        sleep(0.15)
        if len(fila_mensagens) != 0:
            print(fila_mensagens)
            for mensagem in fila_mensagens:
                clientSocket.sendto((json.dumps(mensagem)).encode(), (servidor, port))
            fila_mensagens.clear()



thread_envio_mensagem = threading.Thread(target=metodo_recebimento_mensagens, args=(fila_mensagens_para_envio, ))
thread_envio_mensagem.start()

thread_recebimento_mensagem = threading.Thread(target=metodo_envio_mensagens, args=(fila_mensagens_para_envio, ))
thread_recebimento_mensagem.start()