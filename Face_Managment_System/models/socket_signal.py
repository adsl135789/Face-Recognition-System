import socket
import os, sys
import configparser
from PyQt5.QtCore import QThread


config = configparser.ConfigParser()
config_path = os.path.join(os.getcwd(), "data/config.ini")
config.read(config_path)

class SSignal(QThread):
    def __init__(self, exec_command) -> None:
        super().__init__()
        self.door1 = (config['socket']['door1_ip'],int(config['socket']['door1_port']))
        self.door2 = (config['socket']['door2_ip'],int(config['socket']['door2_port']))
        print(self.door1)

        print(self.door2)

        self.door1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.door2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.door1_socket.settimeout(1)
        self.door2_socket.settimeout(1)
        self.exec_command = exec_command
        self.flag1 = 1
        self.flag2 = 1
        try:
            self.door1_socket.connect(self.door1)
        except Exception as e:
            self.flag1 = 0
            print(f"door1 socket connect failed! {e}")

        try:
            self.door2_socket.connect(self.door2)
        except Exception as e:
            self.flag2 = 0
            print(f"door2 socket connect failed! {e}")

    def run(self):
        if self.flag1:
            self.door1_socket.send(self.exec_command.encode('utf-8'))
        if self.flag2:
            self.door2_socket.send(self.exec_command.encode('utf-8'))
        self.disconnect()

    def disconnect(self):
        if self.flag1:
            self.door1_socket.close()
        if self.flag2:
            self.door2_socket.close()


                
