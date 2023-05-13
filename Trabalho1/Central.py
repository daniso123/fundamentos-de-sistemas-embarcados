from threading import Thread
import socket


ip_servidor = '164.41.98.15'
porta = 10231

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((ip_servidor, porta))

serverSocket.listen(5)

print("Aguardando servidor distribuido . . . ")

# Programa só vai prosseguir se tiver uma conexão
(clientConnected, clientAddress) = serverSocket.accept()

print("Distribuido Conectado")

def receive_messages(fila_respostas):
    while True:
        dataFromClient = clientConnected.recv(1024)
        #print("Data received = " + dataFromClient.decode())
        fila_respostas.append(json.loads(dataFromClient.decode()))
        sleep(0.15)

t = Thread(target=send_messages, args=(fila_instrucoes, ))
t.start()

t2 = Thread(target=receive_messages, args=(fila_respostas, ))
t2.start()