import os
from unittest import TestCase


class BoaTest(TestCase):
    dirname: str = None

    @classmethod
    def setUpClass(cls):
        path = os.path.abspath(__file__).replace('\\', '/')  # for windows compatibility
        cls.dirname = '/'.join(path.split('/')[:-3])

        super(BoaTest, cls).setUpClass()
