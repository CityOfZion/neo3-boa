import os
from typing import Any, Dict, Optional, Tuple
from unittest import TestCase

from boa3.analyser.analyser import Analyser
from boa3.compiler.compiler import Compiler
from boa3.neo3.vm import VMState
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class BoaTest(TestCase):
    dirname: str = None

    ASSERT_RESULTED_FALSE_MSG = 'ASSERT is executed with false result.'
    MAP_KEY_NOT_FOUND_ERROR_MSG = 'Key not found in Map'
    VALUE_IS_OUT_OF_RANGE_MSG = 'The value is out of range'
    STORAGE_VALUE_IS_OUT_OF_RANGE_MSG = 'Specified argument was out of the range of valid values.'

    @classmethod
    def setUpClass(cls):
        cls.dirname = '/'.join(os.path.abspath(__file__).split(os.sep)[:-3])

        super(BoaTest, cls).setUpClass()

    def get_compiler_analyser(self, compiler: Compiler) -> Analyser:
        return compiler._analyser

    def indent_text(self, text: str, no_spaces: int = 4) -> str:
        import re
        return re.sub('\n[ \t]+', '\n' + ' ' * no_spaces, text)

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

    def compile_and_save(self, path: str, log: bool = True) -> Tuple[bytes, Dict[str, Any]]:
        nef_output = path.replace('.py', '.nef')
        manifest_output = path.replace('.py', '.manifest.json')

        from boa3.boa3 import Boa3
        from boa3.neo.contracts.neffile import NefFile
        Boa3.compile_and_save(path, show_errors=log)

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

    def run_smart_contract(self, test_engine: TestEngine, smart_contract_path: str, method: str,
                           *arguments: Any, reset_engine: bool = False,
                           fake_storage: Dict[str, Any] = None) -> Any:

        if smart_contract_path.endswith('.py'):
            if not os.path.isfile(smart_contract_path.replace('.py', '.nef')):
                self.compile_and_save(smart_contract_path, log=False)
            smart_contract_path = smart_contract_path.replace('.py', '.nef')

        if isinstance(fake_storage, dict):
            test_engine.set_storage(fake_storage)

        result = test_engine.run(smart_contract_path, method, *arguments,
                                 reset_engine=reset_engine)

        if test_engine.vm_state is not VMState.HALT and test_engine.error is not None:
            raise TestExecutionException(test_engine.error)
        return result
