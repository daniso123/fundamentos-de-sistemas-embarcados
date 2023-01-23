import time
import serial
from utilitarios.crc16 import calcula_CRC


class UartCommunicator:
    def __init__(self):
        self.serial_port = serial.Serial(port='/dev/serial0', baudrate=9600, timeout=1)
        self.matricula = [4, 9, 9, 2]

    def close_connection(self):
        self.serial_port.close()
        print('connection closed')

    def send_code(self, command_code, valor=b'', tamanho=7):
        if self.serial_port.isOpen():
            m1 = command_code + bytes(self.matricula) + valor
            m2 = calcula_CRC(m1, tamanho).to_bytes(2, 'little')
            msg = m1 + m2
            self.serial_port.write(msg)
        else:
            print('connection refused')
            print("Failed to send message")

    def message_receiver(self):

        time.sleep(0.2)
        buffer = self.serial_port.read(9)
        buffer_size = len(buffer)

        if buffer_size == 9:
            data = buffer[3:7]
            crc16_recebido = buffer[7:9]
            crc16_calculado = calcula_CRC(buffer[0:7], 7).to_bytes(2, 'little')

            if crc16_recebido == crc16_calculado:
                #print('Mensagem recebida: {}'.format(buffer))
                return data
            else:
                print('Mensagem recebida: {}'.format(buffer))
                print('CRC16 invalido')
                return None
        else:
            # print('Mensagem recebida: {}'.format(buffer))
            # print('Mensagem no formato incorreto, tamanho: {}'.format(buffer_size))
            return None