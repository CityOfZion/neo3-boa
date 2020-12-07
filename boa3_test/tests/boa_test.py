import os
from typing import Any, Dict, Iterable, Optional, Tuple, Type
from unittest import TestCase

from boa3.analyser.analyser import Analyser
from boa3.compiler.compiler import Compiler
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3.neo3.vm import VMState
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class BoaTest(TestCase):
    dirname: str = None

    ASSERT_RESULTED_FALSE_MSG = 'ASSERT is executed with false result.'
    MAP_KEY_NOT_FOUND_ERROR_MSG = 'Key not found in Map'
    VALUE_IS_OUT_OF_RANGE_MSG = 'The value is out of range'
    STORAGE_VALUE_IS_OUT_OF_RANGE_MSG = 'Specified argument was out of the range of valid values.'
    CALLED_CONTRACT_DOES_NOT_EXIST_MSG = 'Called Contract Does Not Exist'
    ABORTED_CONTRACT_MSG = 'ABORT is executed'

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

    def get_output(self, path: str) -> Tuple[bytes, Dict[str, Any]]:
        nef_output = path.replace('.py', '.nef')
        manifest_output = path.replace('.py', '.manifest.json')

        from boa3.neo.contracts.neffile import NefFile

        if not os.path.isfile(nef_output):
            output = bytes()
        else:
            with open(nef_output, mode='rb') as nef:
                file = nef.read()
                output = NefFile.deserialize(file).script

        if not os.path.isfile(manifest_output):
            manifest = {}
        else:
            with open(manifest_output) as manifest_output:
                import json
                manifest = json.loads(manifest_output.read())

        return output, manifest

    def run_smart_contract(self, test_engine: TestEngine, smart_contract_path: str, method: str,
                           *arguments: Any, reset_engine: bool = False,
                           fake_storage: Dict[str, Any] = None,
                           signer_accounts: Iterable[bytes] = (),
                           expected_result_type: Type = None) -> Any:

        if smart_contract_path.endswith('.py'):
            if not os.path.isfile(smart_contract_path.replace('.py', '.nef')):
                self.compile_and_save(smart_contract_path, log=False)
            smart_contract_path = smart_contract_path.replace('.py', '.nef')

        if isinstance(fake_storage, dict):
            test_engine.set_storage(fake_storage)

        for account in signer_accounts:
            test_engine.add_signer_account(account)

        result = test_engine.run(smart_contract_path, method, *arguments,
                                 reset_engine=reset_engine)

        if test_engine.vm_state is not VMState.HALT and test_engine.error is not None:
            raise TestExecutionException(test_engine.error)

        if expected_result_type is not None:
            if expected_result_type is not str and isinstance(result, str):
                result = String(result).to_bytes()

            if expected_result_type is bool:
                if isinstance(result, bytes):
                    result = Integer.from_bytes(result, signed=True)
                if isinstance(result, int) and result in (False, True):
                    result = bool(result)

            if expected_result_type is bytearray and isinstance(result, bytes):
                result = bytearray(result)

        return result
