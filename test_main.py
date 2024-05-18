from main import CloudStorage, CloudPicture, SendAnywhere
import unittest


class TestCloudStorage(unittest.TestCase):
    def setUp(self) -> None:
        self.obj1=CloudStorage()
        self.obj2=CloudPicture()

    def test_file_exist(self):
        self.assertTrue(CloudStorage.file_exist("main.py"))
        
    def test_give_filename(self):
        self.assertEqual(self.obj1.give_file_name("/home/samandar/samandar/cloud_project/main.py"), "main.py")
    
    def test_check_filesize(self):
        self.assertIsNotNone(self.obj1.check_file_size("main.py"))
        
    def test_6digit(self):
        self.assertGreater(int(CloudStorage.generate_6_digit_id()), 99999)

    def test_readfile(self):
        self.assertIsNot(self.obj1.read_file("something.html"), "")
        
    def test_store_file(self):
        self.assertGreater(self.obj1.store_file("something.html"), 0)
        
    def test_retrieve(self):
        self.assertIsNone(self.obj1.retrieve_file(123))
        
    def test_vanish_file(self):
        self.assertNotEqual(self.obj1.vanish_file(12), f"File with file_id {12} deleted.")
    
    def test_pic_checksize(self):
        self.assertIsNotNone(self.obj2.check_file_size("ayiq.jpg")) # cloud obj is tested
        
    def test_give_pic_name(self):
        self.assertEqual(self.obj2.give_file_name("/home/samandar/samandar/cloud_project/ayiq.jpg"), "ayiq.jpg")
        


class TestSendAnywhere(unittest.TestCase):
    def setUp(self) -> None:
        self.api_key = "3e72d10d6808518af81b6cf986fae1e4bb839c78"
        self.upload_url = "https://send-anywhere.com/web/v1/key"
        self.device_url="https://send-anywhere.com/web/v1/device"
        self.cookies={}
        self.obj3=SendAnywhere()
        
    def test_apikey(self):
        self.assertEqual(self.obj3.api_key, self.api_key)
        
    def test_device_url(self):
        self.assertEqual(self.obj3.device_url, self.device_url)
        
    def test_upload_url(self):
        self.assertEqual(self.obj3.upload_url, self.upload_url)
    
    
    
        
if __name__ == '__main__':
    unittest.main()       
    
