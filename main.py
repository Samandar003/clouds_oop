# Clouds
import os, sqlite3
from utils import generate_6_digit_id
import time

class CloudStorage:
    def __init__(self) -> None:
        connection=sqlite3.connect('storage.db')

        # self.__file_path=file_path
        # self.size=os.path.getsize(self.get_file_path())

    # def get_file_path(self):
    #     return self.__file_path
    
    # def set_file_path(self, file_path):
    #     self.__file_path=file_path
    
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
            cursor.execute('''CREATE TABLE IF NOT EXISTS Files (id INTEGER PRIMARY KEY, file_id INTEGER, content BLOB, timestamp INTEGER)''')
            timestamp = int(time.time())  
            cursor.execute('''INSERT INTO Files (file_id, content, timestamp) VALUES (?, ?, ?)''', (file_id, CloudStorage.read_file(file_path), timestamp))
            connection.commit()
            print("Stored... File_id ",file_id)
        except sqlite3.Error as e:
            print(f"Error: SQLite error - {e}")
        finally:
            connection.close()
    
    def retrieve_file(self, file_id):
        try:
            connection = sqlite3.connect('storage.db')
            cursor = connection.cursor()
            cursor.execute('''SELECT content FROM Files WHERE file_id = ?''', (file_id,))
            file_content = cursor.fetchone()[0]
            connection.close()
            print(file_content)
        except sqlite3.Error as er:
            print(er)
            return None
        finally:
            connection.close()
    
    def vanish_file(self, file_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute('''DELETE FROM Files WHERE file_id = ?''', (file_id,))
            print(f"File with file_id {file_id} deleted.")
        except sqlite3.Error as e:
            print(f"Error: SQLite error - {e}")

class SendAnywhere(CloudStorage):
    token="3e72d10d6808518af81b6cf986fae1e4bb839c78"
    
    
class StoreTelegram(CloudStorage):
    pass
    
obj=CloudStorage()
# obj.store_file('sql_help.py')
obj.retrieve_file(403027)
