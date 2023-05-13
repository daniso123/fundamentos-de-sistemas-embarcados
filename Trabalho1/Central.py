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