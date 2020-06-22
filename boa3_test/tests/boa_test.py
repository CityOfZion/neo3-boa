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
        return compiler._analyser

    def assertCompilerLogs(self, expected_logged_exception, path):
        with self.assertLogs() as log:
            from boa3.exception.NotLoadedException import NotLoadedException
            try:
                from boa3.boa3 import Boa3
                output = Boa3.compile(path)
            except NotLoadedException:
                # when an compiler error is logged this exception is raised.
                pass

        for logger in log.records:
            import logging
            logging.log(level=logger.levelno, msg=logger.msg)

        if len([exception for exception in log.records if isinstance(exception.msg, expected_logged_exception)]) <= 0:
            raise AssertionError('{0} not logged'.format(expected_logged_exception.__name__))
