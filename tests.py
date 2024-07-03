import unittest
from consts import *
from yadisk.yandex_disk import *
from yadisk.exceptions.ServerError import *
from yadisk.exceptions.InvalidTokenError import *
from yadisk.exceptions.IncorrectDataError import *


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


if __name__ == '__main__':
    unittest.main()
