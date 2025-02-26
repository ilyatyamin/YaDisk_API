import os.path
import time
import unittest

from consts import *
from yadisk.yandex_disk import *
from yadisk.exceptions.exceptions import *


class Tests(unittest.TestCase):
    def setUp(self):
        self.disk = YaDisk(OAUTH_TOKEN)
        self.not_corr_disk = YaDisk(OAUTH_TOKEN + 'abcde')

    def test_invalid_token_format(self):
        with self.assertRaises(InvalidTokenError):
            obj = YaDisk(None)
        with self.assertRaises(InvalidTokenError):
            obj = YaDisk(0)

    def test_file_exists(self):
        # this files exist
        self.assertTrue(self.disk.file_exists('Мишки.jpg'))
        self.assertTrue(self.disk.file_exists('images/image.HEIC'))

        # this file not exists
        self.assertFalse(self.disk.file_exists('STRANGE_FOLDER/StRanGe.File'))

        # this file is folder
        self.assertFalse(self.disk.file_exists('images'))

        with self.assertRaises(InvalidTokenError):
            self.not_corr_disk.file_exists('some data')

    def test_dir_exists(self):
        # these folders exist
        self.assertTrue(self.disk.dir_exists('images'))
        self.assertTrue(self.disk.dir_exists('another_dir'))

        # these folders not exist
        self.assertFalse(self.disk.dir_exists('STRANGE_FOLDER'))
        self.assertFalse(self.disk.dir_exists('self.disk.dir_exists'))

        # this folder is file, but it exists
        self.assertFalse(self.disk.dir_exists('images/image.HEIC'))
        self.assertTrue(self.disk.file_exists('images/image.HEIC'))

        with self.assertRaises(InvalidTokenError):
            self.not_corr_disk.dir_exists('images')

    def test_get_link(self):
        # main.cpp exists in repo
        self.assertNotEquals(self.disk.get_link('main.cpp'), None)
        self.assertIsInstance(self.disk.get_link('main.cpp'), str)

        with self.assertRaises(InvalidTokenError):
            self.not_corr_disk.get_link('main.cpp')

        with self.assertRaises(FileNotFoundError):
            self.disk.get_link('NOT_EXISTED_FILE.SOME_DATA')

    def test_move_files(self):
        # Real files, can be moved
        self.assertIsInstance(self.disk.move_file('TicketRepository.png', 'folder_new/'), str)
        self.assertIsInstance(self.disk.move_file('folder_new/TicketRepository.png', '/'), str)

        with self.assertRaises(IncorrectDataError):
            # src not exists
            self.disk.move_file('UNKNOWED_FOLDER/UNKNOWN_FILE', 'images/')

        with self.assertRaises(IncorrectDataError):
            # dst not exists
            self.disk.move_file('images/', 'UNKNOWED_FOLDER/Some_DIR/')

        with self.assertRaises(InvalidTokenError):
            self.not_corr_disk.move_file('TicketRepository.png', 'folder_new/')

        # Real files, can be moved
        self.assertIsInstance(self.disk.move_file('Море.jpg', 'folder/'), str)
        self.assertIsInstance(self.disk.move_file('folder/Море.jpg', '/', False), str)
        self.assertIsInstance(self.disk.move_file('Москва.jpg', 'folder/yet_one_folder/'), str)
        self.assertIsInstance(self.disk.move_file('folder/yet_one_folder/Москва.jpg', '/'), str)

        # Test overwriting
        with self.assertRaises(IncorrectDataError):
            self.disk.move_file('Зима.jpg', 'images/', False)

        # Move dirs (can be moved)
        self.assertIsInstance(self.disk.move_file('folder', 'folder_new/'), str)
        # # with moving dirs all files was moved
        # with moving files all previous files was saved
        self.assertTrue(self.disk.file_exists('folder_new/SessionRepository.png'))
        # move back
        self.assertIsInstance(self.disk.move_file('folder_new/folder', '/'), str)

    def test_delete_create_dir(self):
        # Real directory can be deleted
        self.assertIsNone(self.disk.delete_directory('empty_folder'))
        time.sleep(1)  # because deleting dir can be not fast
        # Recreate directory
        self.assertIsInstance(self.disk.make_folder('empty_folder'), str)

        # Fake directories, check exceptions
        with self.assertRaises(IncorrectDataError):
            self.disk.delete_directory('NOT REAL DIRECTORY')

        # Fake directory, path to file
        with self.assertRaises(IncorrectDataError):
            self.disk.delete_directory('Зима.jpg')

        # Incorrect token check
        with self.assertRaises(InvalidTokenError):
            self.not_corr_disk.delete_directory('empty_folder')

        # Check permanent deleting
        self.disk.delete_directory('empty_folder', permanently=True)
        time.sleep(1)
        self.assertIsInstance(self.disk.make_folder('empty_folder'), str)

        # Strange test
        with self.assertRaises(IncorrectDataError):
            self.disk.delete_directory('empty_folder' * 10 ** 4)  # 400 error, because the name is too long

    def test_downloading(self):
        # Real file can be downloaded
        self.assertIsNone(self.disk.download_file('Зима.jpg', '/Users/mrshrimp.it/Desktop/',
                                                  tqdm_enabled=False))
        # Check that file was downloaded
        self.assertTrue(os.path.exists('/Users/mrshrimp.it/Desktop/Зима.jpg'))

        # Try to download folder
        self.assertIsNone(self.disk.download_file('folder', '/Users/mrshrimp.it/Desktop/', tqdm_enabled=False))
        # Check that archive was downloaded
        self.assertTrue(os.path.exists('/Users/mrshrimp.it/Desktop/folder.zip'))

        # Try to download unexisted file
        with self.assertRaises(IncorrectDataError):
            self.disk.download_file('file.file', 'path')

        # Try to download unexisted folder
        with self.assertRaises(IncorrectDataError):
            self.disk.download_file('folder_STR/', 'path')

        # Fake token check
        with self.assertRaises(InvalidTokenError):
            self.not_corr_disk.download_file('folder', '/Users/mrshrimp.it/Desktop/', tqdm_enabled=False)

        # Check TQDM Support and large files downloading (realize as chunk)
        self.assertIsNone(self.disk.download_file('Хлебные крошки.mp4', '/Users/mrshrimp.it/Desktop/'))
        self.assertTrue(os.path.exists('/Users/mrshrimp.it/Desktop/Хлебные крошки.mp4'))

    def test_upload(self):
        # Real file
        self.assertIsNone(self.disk.upload_file('/Users/mrshrimp.it/Desktop/algebra_collooqium_23_24.pdf', '/'))
        self.assertTrue(self.disk.file_exists('/algebra_collooqium_23_24.pdf'), str)

        # Fake token check
        with self.assertRaises(InvalidTokenError):
            self.not_corr_disk.upload_file('/Users/mrshrimp.it/Desktop/algebra_collooqium_23_24.pdf', '/')

        # Check folder upload and inner folder support
        self.assertIsNone(self.disk.upload_file('/Users/mrshrimp.it/Desktop/untitled', '/folder/'))
        self.assertTrue(self.disk.file_exists('folder/untitled/main.cpp'))
        self.assertTrue(self.disk.dir_exists('folder/untitled/cmake-build-debug'))

        self.disk.delete_directory('folder')
        self.disk.delete_file('algebra_collooqium_23_24.pdf')


if __name__ == '__main__':
    unittest.main()
