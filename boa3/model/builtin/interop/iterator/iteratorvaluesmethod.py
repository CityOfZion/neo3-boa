from typing import Dict

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.builtin.interop.iterator.iteratortype import IteratorType
from boa3.model.variable import Variable


class IteratorValuesMethod(InteropMethod):
    def __init__(self, iterator: IteratorType):
        syscall = 'System.Iterator.Values'
        identifier = '-iterator_values'
        args: Dict[str, Variable] = {'self': Variable(iterator)}

        from boa3.model.builtin.interop.enumerator import EnumeratorType
        return_type = EnumeratorType.build(iterator)
        super().__init__(identifier, syscall, args, return_type=return_type)

    @property
    def identifier(self) -> str:
        return '{0}_{1}'.format(self.raw_identifier,
                                '_'.join([x.type.identifier for x in self.args.values()]))

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)
