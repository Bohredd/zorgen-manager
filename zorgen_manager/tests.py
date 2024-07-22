import unittest
from unittest.mock import patch, MagicMock, call
import os
import shutil
import sys

from commands.zorgen_admin import is_ignored_directory, find_manage_py, create_app_directory, update_apps_file, custom_startapp, main

class TestZorgenAdmin(unittest.TestCase):

    def test_diretorio_ignorado(self):

        self.assertTrue(is_ignored_directory(
            'blablabla/venv'
        ))

        self.assertTrue(is_ignored_directory(
            'blablabla/env'
        ))

        self.assertTrue(is_ignored_directory(
            'blablabla/enviroment'
        ))

        self.assertTrue(is_ignored_directory(
            'blablabla/virtualenv'
        ))

    def test_find_manage_py(self):

        with self.assertRaises(FileNotFoundError) as context:
            find_manage_py()
        
        self.assertEqual(str(context.exception), "manage.py not found in non-ignored directories.")

    # fazer create directory
    # fazer update apps files
    # fazer custom start app
    # fazer main com tudo

if __name__ == "__main__":
    unittest.main()