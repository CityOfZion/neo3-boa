from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.variable import Variable


class GetInvocationCounterMethod(InteropMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = '-get_invocation_counter'
        syscall = 'System.Runtime.GetInvocationCounter'
        args: dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=Type.int)


class InvocationCounterProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'invocation_counter'
        getter = GetInvocationCounterMethod()
        super().__init__(identifier, getter)
