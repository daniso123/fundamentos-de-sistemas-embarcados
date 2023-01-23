import time
import struct
from threading import Thread, Event

import utilitarios.teperaturaexterna
import utilitarios.csv
import conexão.uart
import conexão.forno
import utilitarios.pid
import utilitarios.controle

pid = utilitarios.pid.PID()
leitor_temperatura_externa = utilitarios.teperaturaexterna.LeitorTemperaturaExterna()
log = utilitarios.csv.LogManager()
communicator = conexão.uart.UartCommunicator()
temperature_controller = utilitarios.controle.FornoControle()


def turn_on():
    print("Oven set on")
    turn_on_code = b'\x01\x23\xd3'
    communicator.send_code(turn_on_code, b'\x01', 8)
    data_received = communicator.message_receiver()
    received_int = int.from_bytes(data_received, 'little')
    print(received_int)


def turn_off():
    print("Oven set off")
    turn_off_code = b'\x01\x23\xd3'
    communicator.send_code(turn_off_code, b'\x00', 8)
    data_received = communicator.message_receiver()
    received_int = int.from_bytes(data_received, 'little')
    print(received_int)


def start_work():
    print("Oven started working")
    turn_on_code = b'\x01\x23\xd5'
    communicator.send_code(turn_on_code, b'\x01', 8)
    data_received = communicator.message_receiver()
    received_int = int.from_bytes(data_received, 'little')
    print(received_int)


def stop_work():
    print("Oven stop working")
    turn_on_code = b'\x01\x23\xd5'
    communicator.send_code(turn_on_code, b'\x00', 8)
    data_received = communicator.message_receiver()
    received_int = int.from_bytes(data_received, 'little')
    print(received_int)


def send_control_signal(signal_intensity):

    send_control_signal_code = b'\x01\x23\xd1'
    valor = (round(signal_intensity)).to_bytes(4, 'little', signed=True)
    communicator.send_code(send_control_signal_code, valor, 11)
    data_received = communicator.message_receiver()


def watch_for_buttons(oven):

    request_buttons_code = b'\x01\x23\xc3'
    communicator.send_code(request_buttons_code)
    data_received = communicator.message_receiver()

    if data_received is not None:

        button = int.from_bytes(data_received, 'little')

        if button == 161:
            print("[1] pressed")
            oven.on = True
            turn_on()
        elif button == 162:
            print("[2] pressed")
            oven.on = False
            turn_off()
            oven.working = False
            stop_work()
        elif button == 163:
            print("[3] pressed")
            oven.working = True
            start_work()
        elif button == 164:
            print("[4] pressed")
            oven.working = False
            stop_work()

    time.sleep(0.5)


def read_and_update_temperature_target(oven):
    request_temperature_target_code = b'\x01\x23\xc2'
    communicator.send_code(request_temperature_target_code)
    data_received = communicator.message_receiver()
    temp = struct.unpack('f', data_received)[0]
    oven.oven_temperature_target = temp
    print("Target Temperature - " + str(temp))


def read_and_update_oven_temperature(oven):
    request_oven_temperature_code = b'\x01\x23\xc1'
    communicator.send_code(request_oven_temperature_code)
    data_received = communicator.message_receiver()
    temp = struct.unpack('f', data_received)[0]
    oven.internal_temperature = temp
    print("Oven temperature - " + str(temp))


def system_update_routine():

    oven = conexão.forno.ReflowOven()

    while True:

        read_and_update_temperature_target(oven)
        watch_for_buttons(oven)
        read_and_update_oven_temperature(oven)
        watch_for_buttons(oven)
        pid_result = pid.output(oven.oven_temperature_target, oven.internal_temperature)

        if oven.on and oven.working:


            print(pid_result)

            send_control_signal(pid_result)

            if pid_result > 0:
                temperature_controller.heat_the_oven(pid_result)
                temperature_controller.cool_the_oven(0)
            else:
                pid_result = pid_result * -1
                if pid_result < 40:
                    pid_result = 40
                temperature_controller.cool_the_oven(pid_result)
                temperature_controller.heat_the_oven(0)

        log.create_log_entry(leitor_temperatura_externa.get_external_temperature(), oven.internal_temperature, oven.oven_temperature_target, pid_result)


system_routine_thread = Thread(target=system_update_routine, args=())
system_routine_thread.start()