import serial
import os
import configparser
import time
config = configparser.ConfigParser()
config_path = os.path.join(os.getcwd(), "data/config.ini")
config.read(config_path)


class RelayCtl:
    def __init__(self):
        self.port = config['serial']['port']
        self.br = int(config['serial']['baud_rate'])
        self.connect()

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.br)
        except serial.SerialException as e:
            print(f"serial fail : {e}")

    def turn_on(self):
        
        data_turn_on = bytes([0xA0,0x01,0x01,0xA2])
        self.ser.write(data_turn_on)

    def turn_off(self):
        data_turn_off = bytes([0xA0,0x01,0x00,0xA1])

        self.ser.write(data_turn_off)

    def open_door(self):
        self.turn_on()
        time.sleep(1)
        self.turn_off()

    def close(self):
        self.ser.close()

if __name__ == '__main__':
    re = RelayCtl()
    re.turn_on()
    time.sleep(1)
    re.turn_off()



