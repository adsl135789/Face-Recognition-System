import socket
import configparser
import os, sys
import json
from models.database_ctrl import Database
from PyQt5.QtCore import QThread

config = configparser.ConfigParser()

config_path = os.path.join(os.getcwd(), "data/config.ini")
config.read(config_path)


class SocketServer(QThread):
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        try:
            self.local_db = Database(
                host=config["local_db"]["host"],
                password=config["local_db"]["password"],
                user=config["local_db"]["user"],
                database=config["local_db"]["database"]
            )
            # check connection and create table
            self.local_db.create_table()
        except Exception as e:
            raise RuntimeError("Failed to initialize local_db") from e

        try:
            self.remote_db = Database(
                host=config["database"]["host"],
                password=config["database"]["password"],
                user=config["database"]["user"],
                database=config["database"]["database"]
            )
            # check connection
            self.remote_db.connect()
            self.remote_db.disconnect()
        except Exception as e:
            raise RuntimeError("Failed to initialize remote_db") from e

        self.db_copy()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 綁定伺服器到一個特定的主機和埠

        self.server_socket.bind((config['socket']['host_ip'], int(config['socket']['host_port'])))

        # 等待客戶端連線
        self.server_socket.listen(5)
        print(f"等待客戶端連線在 {config['socket']['host_ip']}:{config['socket']['host_port']}...")

        self.client_socket, self.client_address = self.server_socket.accept()
        print(f"已連線到 {self.client_address}")

        while True:
            print("-----socket server is waiting for client's mes-----")
            # 接收客戶端傳來的訊息
            data = self.client_socket.recv(1024).decode('utf-8').split("")

            if not data:
                break

            if data[0] == 'insert':
                self.db_copy()
                pass
            elif data[0] == 'delete':
                print("delete:",data[1])
                self.local_db.delete_data(data[1])
                pass
            elif data[0] == 'deleteAll':
                self.local_db.delete_all_data()
                pass
            else: 
                break
            print(self.local_db.read_data)

    def db_copy(self):
        self.remote_db.connect()
        self.local_db.connect()
        self.remote_db.cursor.execute(f"SELECT * FROM {self.remote_db.table_name}")
        data_to_copy = self.remote_db.cursor.fetchall()
        insert_query = f"INSERT INTO {self.remote_db.table_name} (name, config) VALUES (%s, %s)"

        # 批量插入数据
        for row in data_to_copy:
            id, name, config_json = row
            self.local_db.cursor.execute(insert_query, (name, config_json))

        # 提交變更
        self.local_db.db.commit()
        self.remote_db.disconnect()
        self.local_db.disconnect()
        print("資料複製完成")