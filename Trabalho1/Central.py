from threading import Thread

from time import sleep


import socket

import json


fila_instrucoes = []
fila_respostas = []

ip_servidor = '164.41.98.15'
porta = 10240

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((ip_servidor, porta))

serverSocket.listen(5)

print("Aguardando servidor distribuido . . . ")

# Programa só vai prosseguir se tiver uma conexão
(clientConnected, clientAddress) = serverSocket.accept()

print("Distribuido Conectado")


def abrir_cancela(servidor, porta):
    # Criar uma conexão com o servidor
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((servidor, porta))

    # Enviar comando para abrir a cancela
    comando = "ABRIR_CANCELA"
    clientSocket.send(comando.encode())

    # Fechar a conexão
    clientSocket.close()
