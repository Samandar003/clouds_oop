from main import CloudStorage, CloudPicture
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
    
if __name__ == '__main__':
    unittest.main()       
    
