# LCUS-1 USB Relay command : <lag  Addr CMD CRC>
# Relay On  : A0 01 01 A2
# Relay Off : A0 01 00 A1

import socket
import time
from models.relay_ctl import RelayCtl
from PyQt5.QtCore import QThread



class Lcm(QThread):
    def __init__(self):
        super().__init__()
        # Define the UDP server settings
        self.host = '0.0.0.0'
        self.port = 51688

        # Create a UDP socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the socket to the specified host and port
        self.udp_socket.bind((self.host, self.port))

        print(f"UDP server is listening on {self.host}:{self.port}")

    def run(self):
        while True:
            print("-- waiting -- ")
            # Receive data from a client
            data, address = self.udp_socket.recvfrom(1024)  # Maximum data size is 1024 bytes   
            # Decode the received data from bytes to a string
            received_data = data.decode('utf-8')
            print("Received:", received_data)            

            # Check if the received data matches the expected string
            if received_data == "$0 set unlock":
                print("Received:", received_data)            
                relay = RelayCtl()
                relay.open_door()
                
            else:
                print("Received data does not match the expected string.")