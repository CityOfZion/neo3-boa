import os
from unittest import TestCase

from boa3.analyser.analyser import Analyser
from boa3.compiler.compiler import Compiler


class BoaTest(TestCase):
    dirname: str = None

    @classmethod
    def setUpClass(cls):
        path = os.path.abspath(__file__).replace('\\', '/')  # for windows compatibility
        cls.dirname = '/'.join(path.split('/')[:-3])

        super(BoaTest, cls).setUpClass()

    def get_compiler_analyser(self, compiler: Compiler) -> Analyser:
        return compiler._Compiler__analyser
