from boa3.internal.exception import CompilerError
from boa3_test.tests import boatestcase


class TestSet(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/set_test'

    def test_set_from_typing(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'SetTyping.py')

    def test_set_literal(self):
        self.assertCompilerLogs(CompilerError.InvalidType, 'SetLiteral.py')

    def test_set_from_constructor(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'SetConstructor.py')
