

import unittest
import pathlib
from ElGamal import get_message
from io import StringIO
from contextlib import redirect_stdout


class TestGetMessage(unittest.TestCase):

    def test_invalid_input(self):
        with self.assertRaises(SystemExit):
            get_message(1)

        with self.assertRaises(SystemExit):
            get_message(2.4)

    def test_str_input(self):
        text = "this is a test"
        message = get_message(text)
        self.assertTrue(isinstance(message, str))

    def test_directory_path_input(self):

        path = pathlib.Path()
        with self.assertRaises(IsADirectoryError):
            get_message(path)

    def test_empty_file_path_input(self):

        path = pathlib.Path("test/test_file_empty.txt")
        with self.assertRaises(SystemExit):
            get_message(path)

    def test_byte_file_path_input(self):

        path = pathlib.Path("test/data")
        with self.assertRaises(SystemExit):
            get_message(path)
