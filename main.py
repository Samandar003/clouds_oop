# Clouds
import os, sqlite3
from utils import generate_6_digit_id


class CloudStorage:
    def __init__(self, file_path, type) -> None:
        self.__file_path=file_path
        self.size=os.path.getsize(self.get_file_path())
        self.type=type
        self.file_id=generate_6_digit_id()
        
    def get_file_path(self):
        return self.__file_path
    
    def set_file_path(self, file_path):
        self.__file_path=file_path
        
    
    def store_file(self):
        pass
    
    def retrieve_file(self, file_id):
        pass

class SendAnywhere(CloudStorage):
    token="3e72d10d6808518af81b6cf986fae1e4bb839c78"
    
    
class StoreTelegram(CloudStorage):
    pass
    
obj=CloudStorage("utils.py", 'file')
print(obj.size)


