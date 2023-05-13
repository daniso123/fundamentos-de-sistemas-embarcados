import socket
import json

ip_servidor = '164.41.98.15'
porta = 10231

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((ip_servidor, porta))

print("Cliente conectado ao servidor")

# Exemplo de envio de mensagem para o servidor
mensagem = {
    "acao": "acao_exemplo",
    "dados": "Dados de exemplo"
}
mensagem_json = json.dumps(mensagem)
clientSocket.sendall(mensagem_json.encode())

# Exemplo de recebimento de resposta do servidor
dataFromServer = clientSocket.recv(1024)
resposta = json.loads(dataFromServer.decode())
print("Resposta do servidor:", resposta)

# Fechar a conexão com o servidor
clientSocket.close()
