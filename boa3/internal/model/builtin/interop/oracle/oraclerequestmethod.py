from boa3.internal.model.builtin.interop.nativecontract import OracleMethod
from boa3.internal.model.variable import Variable


class OracleRequestMethod(OracleMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type

        identifier = 'request'
        syscall = 'request'
        args: dict[str, Variable] = {'url': Variable(Type.str),
                                     'request_filter': Variable(Type.str),
                                     'callback': Variable(Type.str),
                                     'user_data': Variable(Type.any),
                                     'gas_for_response': Variable(Type.int)}

        super().__init__(identifier, syscall, args, return_type=Type.none)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None
