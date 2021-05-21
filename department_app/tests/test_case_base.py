import unittest

from department_app import app


class TestCaseBase(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        self.client = app.test_client()