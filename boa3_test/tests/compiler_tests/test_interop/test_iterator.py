from typing import cast

from boaconstructor import storage

from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.neo.vm.type.String import String
from boa3_test.tests import boatestcase


class TestIteratorInterop(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/interop_test/iterator'

    def test_iterator_create(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'IteratorCreate.py')

    async def test_iterator_next(self):
        await self.set_up_contract('IteratorNext.py')

        prefix = b'test_iterator_next'
        result, _ = await self.call('has_next', [prefix], return_type=bool)
        self.assertEqual(False, result)

        key = prefix + b'example1'
        value = 1
        await self.call('store_data', [key, value], return_type=None, signing_accounts=[self.genesis])

        contract_storage = cast(
            dict[bytes, int],
            await self.get_storage(
                prefix=prefix,
                values_post_processor=storage.as_int
            )
        )
        self.assertIn(key, contract_storage)
        self.assertEqual(value, contract_storage[key])

        result, _ = await self.call('has_next', [prefix], return_type=bool)
        self.assertEqual(True, result)

    async def test_iterator_value(self):
        await self.set_up_contract('IteratorValue.py')

        prefix = b'test_iterator_value'
        result, _ = await self.call('test_iterator', [prefix], return_type=None)
        self.assertIsNone(result)

        key = prefix + b'example1'
        await self.call('store_data', [key, 1], return_type=None, signing_accounts=[self.genesis])

        contract_storage = cast(
            dict[bytes, int],
            await self.get_storage(
                prefix=prefix
            )
        )
        self.assertIn(key, contract_storage)

        result, _ = await self.call('test_iterator', [prefix], return_type=tuple[bytes, bytes])
        self.assertEqual((key, contract_storage[key]), result)

    def test_iterator_value_dict_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'IteratorValueMismatchedType.py')

    async def test_import_iterator(self):
        await self.set_up_contract('ImportIterator.py')

        # TODO: #86drqwhx0 neo-go in the current version of boa-test-constructor is not configured to return Iterators
        with self.assertRaises(ValueError) as context:
            result, _ = await self.call('return_iterator', [], return_type=list)
            self.assertEqual([], result)

        self.assertRegex(str(context.exception), 'Interop stack item only supports iterators')

    async def test_import_interop_iterator(self):
        self.assertCompilerLogs(CompilerWarning.DeprecatedSymbol, 'ImportInteropIterator.py')
        await self.set_up_contract('ImportInteropIterator.py')

        # TODO: #86drqwhx0 neo-go in the current version of boa-test-constructor is not configured to return Iterators
        with self.assertRaises(ValueError) as context:
            result, _ = await self.call('return_iterator', [], return_type=list)
            self.assertEqual([], result)

        self.assertRegex(str(context.exception), 'Interop stack item only supports iterators')

    async def test_iterator_implicit_typing(self):
        await self.set_up_contract('IteratorImplicitTyping.py')

        prefix = b'test_iterator_'
        prefix_str = String.from_bytes(prefix)
        result, _ = await self.call('search_storage', [prefix], return_type=dict[str, int])
        self.assertEqual({}, result)

        result, _ = await self.call('store', [prefix + b'1', 1], return_type=None, signing_accounts=[self.genesis])
        self.assertIsNone(result)

        result, _ = await self.call('store', [prefix + b'2', 2], return_type=None, signing_accounts=[self.genesis])
        self.assertIsNone(result)

        result, _ = await self.call('search_storage', [prefix], return_type=dict[str, int])
        self.assertEqual({f'{prefix_str}1': 1, f'{prefix_str}2': 2}, result)

    async def test_iterator_value_access(self):
        await self.set_up_contract('IteratorValueAccess.py')

        prefix = b'test_iterator_'
        prefix_str = String.from_bytes(prefix)
        result, _ = await self.call('search_storage', [prefix], return_type=dict[str, int])
        self.assertEqual({}, result)

        result, _ = await self.call('store', [prefix + b'1', 1], return_type=None, signing_accounts=[self.genesis])
        self.assertIsNone(result)

        result, _ = await self.call('store', [prefix + b'2', 2], return_type=None, signing_accounts=[self.genesis])
        self.assertIsNone(result)

        result, _ = await self.call('search_storage', [prefix], return_type=dict[str, int])
        self.assertEqual({f'{prefix_str}1': 1, f'{prefix_str}2': 2}, result)
