from boa3.internal.exception import CompilerError
from boa3_test.tests import boatestcase


class TestMath(boatestcase.BoaTestCase):

    default_folder: str = 'test_sc/math_test'

    def test_no_import(self):
        path = self.get_contract_path('NoImport.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    # region pow test

    async def test_pow_method(self):
        await self.set_up_contract('Pow.py')
        import math

        base = 1
        exponent = 4
        result, _ = await self.call('main', [base, exponent], return_type=int)
        self.assertEqual(math.pow(base, exponent), result)

        base = 5
        exponent = 2
        result, _ = await self.call('main', [base, exponent], return_type=int)
        self.assertEqual(math.pow(base, exponent), result)

        base = -2
        exponent = 2
        result, _ = await self.call('main', [base, exponent], return_type=int)
        self.assertEqual(math.pow(base, exponent), result)

        base = -2
        exponent = 3
        result, _ = await self.call('main', [base, exponent], return_type=int)
        self.assertEqual(math.pow(base, exponent), result)

        base = 2
        exponent = 0
        result, _ = await self.call('main', [base, exponent], return_type=int)
        self.assertEqual(math.pow(base, exponent), result)

    async def test_pow_method_from_math(self):
        await self.set_up_contract('PowFromMath.py')
        from math import pow

        base = 2
        exponent = 3
        result, _ = await self.call('main', [base, exponent], return_type=int)
        self.assertEqual(pow(base, exponent), result)

    # endregion

    # region sqrt test

    async def test_sqrt_method(self):
        await self.set_up_contract('MathSqrt.py')
        from math import sqrt

        radicand = 0
        result, _ = await self.call('main', [radicand], return_type=int)
        self.assertEqual(int(sqrt(radicand)), result)

        radicand = 1
        result, _ = await self.call('main', [radicand], return_type=int)
        self.assertEqual(int(sqrt(radicand)), result)

        radicand = 3
        result, _ = await self.call('main', [radicand], return_type=int)
        self.assertEqual(int(sqrt(radicand)), result)

        radicand = 4
        result, _ = await self.call('main', [radicand], return_type=int)
        self.assertEqual(int(sqrt(radicand)), result)

        radicand = 8
        result, _ = await self.call('main', [radicand], return_type=int)
        self.assertEqual(int(sqrt(radicand)), result)

        radicand = 10
        result, _ = await self.call('main', [radicand], return_type=int)
        self.assertEqual(int(sqrt(radicand)), result)

        radicand = 25
        result, _ = await self.call('main', [radicand], return_type=int)
        self.assertEqual(int(sqrt(radicand)), result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [-1], return_type=int)

        self.assertRegex(str(context.exception), 'negative value')

    async def test_sqrt_method_from_math(self):
        await self.set_up_contract('MathSqrtFromMath.py')
        from math import sqrt

        val = 25
        result, _ = await self.call('main', [val], return_type=int)
        self.assertEqual(int(sqrt(val)), result)

    # endregion
