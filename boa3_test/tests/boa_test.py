import os
from typing import Any, Dict, Optional, Tuple
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
        output = None
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
        return output

    def compile_and_save(self, path: str) -> Tuple[bytes, Dict[str, Any]]:
        nef_output = path.replace('.py', '.nef')
        manifest_output = path.replace('.py', '.manifest.json')

        from boa3.boa3 import Boa3
        from boa3.neo.contracts.neffile import NefFile
        Boa3.compile_and_save(path)

        with open(nef_output, mode='rb') as nef:
            file = nef.read()
            output = NefFile.deserialize(file).script

        with open(manifest_output) as manifest_output:
            import json
            manifest = json.loads(manifest_output.read())

        return output, manifest

    def get_debug_info(self, path: str) -> Optional[Dict[str, Any]]:
        debug_info_output = path.replace('.py', '.nefdbgnfo')

        if not os.path.isfile(debug_info_output):
            return None

        from zipfile import ZipFile
        with ZipFile(debug_info_output, 'r') as dbgnfo:
            import json
            debug_info = json.loads(dbgnfo.read(os.path.basename(path.replace('.py', '.debug.json'))))
        return debug_info
