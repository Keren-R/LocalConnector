import os.path
import shutil
from typing import List
from unittest import TestCase

from local_connector import LocalConnector

LIMITED_ACCESS = 0o000
DEFAULT_ACCESS = 0o777


def create_new_text_file(file_name: str, dir_path: str, chmod: int) -> str:
    file_name = f"{file_name}.txt"
    file_path = os.path.join(dir_path,file_name)
    with open(file_path, 'w') as fp:
        pass

    os.chmod(file_path, mode=chmod)

    return file_path


def empty_directory(dir_path: str):
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


class TestLocalConnector(TestCase):
    local_dir_path = None
    remote_dir_source = None
    connector: LocalConnector

    @classmethod
    def setUpClass(cls):
        cls.connector = LocalConnector(connection_id="")
        cls.remote_dir_source = "/home/keren/Desktop/remote_host"
        cls.remote_path = create_new_text_file("new_file", cls.remote_dir_source, DEFAULT_ACCESS)
        cls.permission_limited_file_path = create_new_text_file("permission_limited", cls.remote_dir_source, LIMITED_ACCESS)
        cls.local_dir_path = os.path.join(os.curdir, "local_storage")
        cls.fake_path = "some/fake/path"

    def test_download_file(self):
        assert self.connector.download_file(self.remote_path, self.local_dir_path)
        assert os.path.exists(os.path.join(self.local_dir_path, "new_file.txt"))

        self.assertFalse(self.connector.download_file(self.fake_path, self.fake_path))
        self.assertFalse(self.connector.download_file(self.remote_path, self.fake_path))
        self.assertFalse(self.connector.download_file(self.remote_path, self.remote_path))
        self.assertFalse(self.connector.download_file(self.local_dir_path, self.local_dir_path))

        self.assertFalse(self.connector.download_file(self.permission_limited_file_path, self.local_dir_path))

    def test_remove_local_file(self):
        file_path = os.path.join(self.local_dir_path, "new_file.txt")
        self.assertTrue(self.connector.remove_local_file(file_path))
        self.assertFalse(self.connector.remove_local_file(self.fake_path))

    def test_get_last_modification_time(self):
        self.assertNotEqual(self.connector.get_last_modification_time(self.remote_path), 0.0)
        self.assertEqual(self.connector.get_last_modification_time(self.fake_path), 0.0)

    def test_get_directory_tree(self):
        assert self.connector.get_directory_tree(os.path.curdir)
        self.assertSequenceEqual(self.connector.get_directory_tree(self.fake_path), [])

    @classmethod
    def tearDownClass(cls):
        empty_directory(cls.remote_dir_source)
        empty_directory(cls.local_dir_path)