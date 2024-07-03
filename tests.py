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

    def test_fileexists(self):
        self.assertTrue(self.disk.file_exists('Мишки.jpg'))
        self.assertTrue(self.disk.file_exists('images/image.HEIC'))

        self.assertFalse(self.disk.file_exists('STRANGE_FOLDER/StRanGe.File'))

        with self.assertRaises(InvalidTokenError):
            self.not_corr_disk.file_exists('some data')


    def test_getlink(self):
        # main.cpp exists in repo
        self.assertNotEquals(self.disk.get_link('main.cpp'), None)
        self.assertIsInstance(self.disk.get_link('main.cpp'), str)

        with self.assertRaises(InvalidTokenError):
            self.not_corr_disk.get_link('main.cpp')

        with self.assertRaises(FileNotFoundError):
            self.disk.get_link('NOT_EXISTED_FILE.SOME_DATA')


if __name__ == '__main__':
    unittest.main()
