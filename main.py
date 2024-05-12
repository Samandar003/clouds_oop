# Clouds
import os, sqlite3
from utils import generate_6_digit_id
import time
import requests
import json

class CloudStorage:
    def __init__(self) -> None:
        self.connection=sqlite3.connect('storage.db')
        self.table="Files"
        max_file_size=10 #mb
        # self.__file_path=file_path
        # self.size=os.path.getsize(self.get_file_path())

    # def get_file_path(self):
    #     return self.__file_path
    
    # def set_file_path(self, file_path):
    #     self.__file_path=file_path
    
    @staticmethod
    def file_exist(file):
        return os.path.exists(file)
    
    def check_file_size(self, file):
        if CloudStorage.file_exist(file):
            return os.path.getsize(file)
        return 0
    
    @staticmethod
    def read_file(file_path):
        try:
            with open(file_path, 'rb') as file:
                file_content=file.read()
            return file_content
        except:
            print(f"{file_path} not found")
            return None
    
    def store_file(self, file_path):
        file_id=generate_6_digit_id()
        try:
            connection=sqlite3.connect('storage.db')
            cursor=connection.cursor()
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table} (id INTEGER PRIMARY KEY, file_id INTEGER, content BLOB, timestamp INTEGER)''')
            timestamp = int(time.time())  
            cursor.execute(f'''INSERT INTO {self.table} (file_id, content, timestamp) VALUES (?, ?, ?)''', (file_id, CloudStorage.read_file(file_path), timestamp))
            connection.commit()
            return file_id
        except sqlite3.Error as e:
            print(f"Error: SQLite error - {e}")
        finally:
            connection.close()
    
    def retrieve_file(self, file_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f'''SELECT content FROM {self.table} WHERE file_id = ?''', (file_id,))
            file_content = cursor.fetchone()[0]
            self.connection.close()
            print(file_content)
        except sqlite3.Error as er:
            print(er)
            return None
        finally:
            self.connection.close()
    
    def vanish_file(self, file_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f'''DELETE FROM {self.table} WHERE file_id = ?''', (file_id,))
            print(f"File with file_id {file_id} deleted.")
        except sqlite3.Error as e:
            print(f"Error: SQLite error - {e}")



class SendAnywhere(CloudStorage):
    def __init__(self):
        self.api_key = "3e72d10d6808518af81b6cf986fae1e4bb839c78"
        self.upload_url = "https://send-anywhere.com/web/v1/key"
        self.device_url="https://send-anywhere.com/web/v1/device"
        self.cookies={}
        
    def store_file(self, file_path):
        try:
            data = requests.get(self.device_url, auth=(self.api_key, ''))
            device_key = data.json()['device_key']
            
            data = {"file": [{"name": "/home/samandar/samandar/labnotes-beta.pdf", "size": 2}]}
            json_data = json.dumps(data)
            self.cookies={'device_key':device_key}
            response=requests.get(self.upload_url, params=json_data, cookies=self.cookies)
            print(response.text)
            
            if response.status_code == 200:
                return response.json()['weblink']
            else:
                print(f"Error: Failed to upload the file. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        
        
    def receieve_file(self, key, web_link):
        download_url="https://send-anywhere.com/web/v1/key/{key}"
        params={"key":key, "weblink":web_link}
        response = requests.get(download_url, params=params, cookies=self.cookies)
        if response.status_code==200:
            return response.text
    
    
obj=CloudStorage()
# obj.store_file('sql_help.py')
# obj.retrieve_file(403027)
obj2=SendAnywhere()
obj2.store_file("sql_help.py")

