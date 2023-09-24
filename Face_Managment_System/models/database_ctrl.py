import json
import pymysql
import os,sys
import socket
from pymysql import err

class Database:
    def __init__(self, host='localhost', user='root', password='0000', database='faces'):
        self.cursor = None
        self.db = None
        self.host = host
        self.user = user 
        self.password = password
        self.database = database
        self.table_name = "table_faces"
        self.create_database_if_not_exists()

    def create_database_if_not_exists(self):
        try:
            connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            connection.close()
        except pymysql.MySQLError as e:
            if "Unknown database" in str(e):
                connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    port=3306
                )
                cursor = connection.cursor()

                create_database_squry = f"CREATE DATABASE {self.database}"
                cursor.execute(create_database_squry)

                connection.commit()
                print(f"Create database {self.database}")

                cursor.close()
                connection.close()

    def connect(self):
        self.db = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        self.cursor = self.db.cursor()

    def disconnect(self):
        try:
            self.cursor.close()
            self.db.close()
        except err.Error as e:
            if "Already closed" in str(e):
                pass  # 忽略已关闭连接的异常
            else:
                raise  # 重新引发其他异常


    def create_table(self):
        self.connect()
        # Create table as per requirement
        sql = f"""
              CREATE TABLE IF NOT EXISTS {self.table_name} (
                  id INT AUTO_INCREMENT PRIMARY KEY,
                  name VARCHAR(20),
                  config JSON
              )"""

        self.cursor.execute(sql)
        self.db.commit()
        self.disconnect()
        print("Created table Successfull.")

    def insert_data(self, name, config):
        self.connect()
        insert_query = f"INSERT INTO {self.table_name} (name, config) VALUES (%s, %s)"
        config_str = json.dumps(config)
        self.cursor.execute(insert_query, (name, config_str))
        self.db.commit()
        print(f"Inserted data: name='{name}'")
        print(self.read_data())
        self.disconnect()

    # 读取数据
    def read_data(self):
        self.connect()
        select_query = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(select_query)
        results = self.cursor.fetchall()
        config_json_list = []
        if not results:
            print("db is empty.")
            return results
        for row in results:
            id, name, config_json = row
            config = json.loads(config_json)
            config_json_list.append(config)
        self.disconnect()
        return config_json_list

    def read_someone_data(self, name):
        self.connect()
        select_query = f"SELECT * FROM {self.table_name} WHERE name = %s"
        self.cursor.execute(select_query, (name,))
        results = self.cursor.fetchall()
        config_json_list = []
        if not results:
            print(f"There is no {name=} in the {self.table_name=}")
            return results
        for row in results:
            id, name, config_json = row
            config = json.loads(config_json)
            config_json_list.append(config)
        self.disconnect()
        return config_json_list

    # 删除数据
    def delete_data(self, name):
        self.connect()
        delete_query = f"DELETE FROM {self.table_name} WHERE name = %s"
        self.cursor.execute(delete_query, (name,))
        self.db.commit()
        print(f"Deleted data with name: {name}")
        self.disconnect()

    def delete_all_data(self):
        self.connect()
        delete_query = f"""
            DELETE FROM {self.table_name}
            WHERE JSON_EXTRACT(config, '$.isSupervisor') != true;
            """
        self.cursor.execute(delete_query)
        self.db.commit()
        print(f"Deleted all data")
        self.disconnect()

    def find_user(self, name):
        self.connect()
        find_query = f"SELECT * FROM {self.table_name} WHERE name = %s"
        self.cursor.execute(find_query, (name,))
        result = self.cursor.fetchall()
        self.disconnect()
        return result
