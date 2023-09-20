# LCUS-1 USB Relay command : <lag  Addr CMD CRC>
# Relay On  : A0 01 01 A2
# Relay Off : A0 01 00 A1

import socket
import serial
import time
# Define the UDP server settings
host = '0.0.0.0'  # Listen on all available network interfaces
port = 51688

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the specified host and port
udp_socket.bind((host, port))

print(f"UDP server is listening on {host}:{port}")

while True:
    # Receive data from a client
    data, address = udp_socket.recvfrom(1024)  # Maximum data size is 1024 bytes
    
    # Decode the received data from bytes to a string
    received_data = data.decode('utf-8')
    
    # Check if the received data matches the expected string
    if received_data == "$0 set unlock":
        print("Received:", received_data)
        com_port = 'COM4'
        baud_rate = 9600
        data_bits = 8
        stop_bits = 1
        parity = serial.PARITY_NONE

        # Create a serial port object
        ser = serial.Serial(com_port, baud_rate, bytesize=data_bits, stopbits=stop_bits, parity=parity)

        # Open Relay in HEX value command
        hex_value = bytes.fromhex('A0 01 01 A2')
        ser.write(hex_value)

        time.sleep(5)

        # Close Relay
        hex_value = bytes.fromhex('A0 01 00 A1')
        ser.write(hex_value)

        # Close the serial port when done
        ser.close()        
        
        
    else:
        print("Received data does not match the expected string.")