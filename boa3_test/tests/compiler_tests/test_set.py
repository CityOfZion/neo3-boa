from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError


class TestSet(BoaTest):
    default_folder: str = 'test_sc/set_test'

    def test_set_from_typing(self):
        path = self.get_contract_path('SetTyping.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_set_literal(self):
        path = self.get_contract_path('SetLiteral.py')
        self.assertCompilerLogs(CompilerError.InvalidType, path)

    def test_set_from_constructor(self):
        path = self.get_contract_path('SetConstructor.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)
