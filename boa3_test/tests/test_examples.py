from boa3_test.tests.boa_test import BoaTest


class TestTemplate(BoaTest):

    def test_nep5(self):
        path = '%s/boa3_test/examples/nep5.py' % self.dirname
        output, manifest = self.compile_and_save(path)
