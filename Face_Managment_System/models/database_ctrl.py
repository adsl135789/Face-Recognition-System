import json
import pymysql


class Database:
    def __init__(self, host='localhost', user='root', password='0000', database='faces'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.db = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.db.cursor()
        self.table_name = "table_faces"

    def create_table(self):
        # Create table as per requirement
        sql = f"""
              CREATE TABLE IF NOT EXISTS {self.table_name} (
                  id INT AUTO_INCREMENT PRIMARY KEY,
                  name VARCHAR(20),
                  config JSON
              )"""

        self.cursor.execute(sql)
        self.db.commit()
        print("Created table Successfull.")

    def insert_data(self, name, config):
        insert_query = f"INSERT INTO {self.table_name} (name, config) VALUES (%s, %s)"
        config_str = json.dumps(config)
        self.cursor.execute(insert_query, (name, config_str))
        self.db.commit()
        print(f"Inserted data: name='{name}'")
        print(self.read_data())

    # 读取数据
    def read_data(self):
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
        return config_json_list

    def read_someone_data(self, name):
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
        return config_json_list

    # 删除数据
    def delete_data(self, name):
        delete_query = f"DELETE FROM {self.table_name} WHERE name = %s"
        self.cursor.execute(delete_query, (name,))
        self.db.commit()
        print(f"Deleted data with name: {name}")

    def delete_all_data(self):
        delete_query = f"DELETE FROM {self.table_name}"
        self.cursor.execute(delete_query)
        self.db.commit()
        print(f"Deleted all data")

    def find_user(self, name):
        find_query = f"SELECT * FROM {self.table_name} WHERE name = %s"
        self.cursor.execute(find_query, (name,))
        result = self.cursor.fetchall()
        return result
