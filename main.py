# Clouds
import os, sqlite3
import time
import requests
import json
import random

class CloudStorage:
    counts=0
    def __init__(self) -> None:
        self.connection=sqlite3.connect('storage.db')
        self.table="Files"
        self.__max_file_size=10 #mb
        CloudStorage.count+=1   # to
    
    @classmethod  # that variable is owned by class, cls is the best way to access
    def count_objs(cls):
        return cls.count 
    
    @staticmethod
    def file_exist(file):
        return os.path.exists(file)
    
    def give_file_name(self, file_path):
        return os.path.basename(file_path)
    
    def check_file_size(self, file):
        if CloudStorage.file_exist(file):
            file_size=os.path.getsize(file)/(1024 * 1024)
            if file_size<11:
                return file_size
        return None
    
    @staticmethod
    def generate_6_digit_id():
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])

    
    def read_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                file_content=file.read()
            return file_content
        except:
            print(f"{file_path} not found")
            return None
    
    def store_file(self, file_path):
        if self.check_file_size(file_path) is not None:
            file_id=CloudStorage.generate_6_digit_id()
            try:
                connection=sqlite3.connect('storage.db')
                cursor=connection.cursor()
                file_name=self.give_file_name(file_path)
                cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table} (id INTEGER PRIMARY KEY, file_name TEXT, file_id INTEGER, content BLOB, timestamp INTEGER)''')
                timestamp = int(time.time())  
                cursor.execute(f'''INSERT INTO {self.table} (file_name, file_id, content, timestamp) VALUES (?, ?, ?, ?)''', (file_name, file_id, self.read_file(file_path), timestamp))
                connection.commit()
                return file_id
            except sqlite3.Error as e:
                print(f"Error: SQLite error - {e}")
            finally:
                connection.close()
        return "FIle size exceeding"
        
    def retrieve_file(self, file_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f'''SELECT file_name, content FROM {self.table} WHERE file_id = ?''', (file_id,))
            name_content = cursor.fetchone()
            file_name, file_content = name_content
            file_path = os.path.join("downloads", file_name)
            with open(file_path, 'wb') as file:
                file.write(file_content)
            self.connection.close()
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

class CloudPicture(CloudStorage):
    def __init__(self) -> None:
        super().__init__()
        self.table="Pictures"
        self.__max_size=5

class SendAnywhere(CloudStorage):
    def __init__(self):
        self.api_key = "3e72d10d6808518af81b6cf986fae1e4bb839c78"
        self.upload_url = "https://send-anywhere.com/web/v1/key"
        self.device_url="https://send-anywhere.com/web/v1/device"
        self.cookies={}
        
    def store_file(self, file_path):   # method overriding
        try:
            if self.check_file_size(file_path) is not None:
                file_cont=self.read_file(file_path)
                data = requests.get(self.device_url, auth=(self.api_key, ''))
                device_key = data.json()['device_key']
                data_p = {"file": [{"name": file_path, "size": 32.2}]}
                print(data_p)
                self.cookies={'device_key':device_key}
                response=requests.get(self.upload_url, params=data_p, cookies=self.cookies)
                print(response.text)
                
                if response.status_code == 200:
                    return response.json()['weblink']
                else:
                    print(f"Error: Failed to upload the file. Status code: {response.status_code}")
                    return None
            return "File Not FOUND"
        except Exception as e:
            print(f"Error: {e}")
            return None
        
        
    def receieve_file(self, key, web_link): # method overloading
        download_url="https://send-anywhere.com/web/v1/key/{key}"
        params={"key":key, "weblink":web_link}
        response = requests.get(download_url, params=params, cookies=self.cookies)
        if response.status_code==200:
            return response.text
        
        
    def vanish_file(self, file_id=None):   # in sendanywhere , it is automatically deleted after 10 mins
        pass
        


obj=CloudStorage()
# print(obj.store_file("utils.py"))
obj.retrieve_file("072621")


# obj=SendAnywhere()
# obj.store_file("/home/samandar/samandar/1.pdf")

# print(obj.store_file("/home/samandar/samandar/ma0405b.pdf"))
# obj.retrieve_file()

# obj.retrieve_file(403027)
# obj2=SendAnywhere()
# obj2.store_file("/home/samandar/samandar/labnotes-beta.pdf")


