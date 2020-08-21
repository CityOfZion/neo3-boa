from boa3.boa3 import Boa3
from boa3_test.tests.boa_test import BoaTest


class TestTemplate(BoaTest):

    def test_nep5(self):
        path = '%s/boa3_test/examples/nep5.py' % self.dirname
        output = Boa3.compile(path)
