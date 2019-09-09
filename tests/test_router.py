import os
import unittest
from deez import Deez
from deez.router import Router


class RouterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        os.environ.setdefault('PROJECT_SETTINGS_MODULE', 'settings')
        app = Deez()
        self.router = Router(app)

    def test_route(self):
        pass