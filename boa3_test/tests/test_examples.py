from boa3_test.tests.boa_test import BoaTest


class TestTemplate(BoaTest):

    def test_nep5(self):
        # TODO: include result tests when the test engine integration is implemented
        path = '%s/boa3_test/examples/nep5.py' % self.dirname
        output, manifest = self.compile_and_save(path)

    def test_ico(self):
        # TODO: include result tests when the test engine integration is implemented
        path = '%s/boa3_test/examples/ico.py' % self.dirname
        output, manifest = self.compile_and_save(path)
