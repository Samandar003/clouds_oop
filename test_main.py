from main import CloudStorage, CloudPicture
import unittest


class TestCloudStorage(unittest.TestCase):
    def setUp(self) -> None:
        self.obj1=CloudStorage()
        self.obj2=CloudPicture()

    def test_file_exist(self):
        self.assertTrue(CloudStorage.file_exist("main.py"))
        
    def test_give_filename(self):
        self.assertEqual("/home/samandar/samandar/cloud_project/main.py", "main.py")
    
    def test_check_filesize(self):
        self.assertIsNotNone(self.obj("main.py"))
        
    def test_6digit(self):
        self.assertGreater(CloudStorage.generate_6_digit_id(), 99999)

    def test_readfile(self):
        self.assertEqual(self.obj1.read_file("something.html"), "<!DOCTYPE html>")
        
    
