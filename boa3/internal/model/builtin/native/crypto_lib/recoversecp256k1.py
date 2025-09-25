from boa3.internal.model.builtin.interop.nativecontract import CryptoLibMethod
from boa3.internal.model.variable import Variable


class RecoverSecp256K1Method(CryptoLibMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type

        identifier = 'recover_secp256k1'
        syscall = 'recoverSecp256K1'
        args: dict[str, Variable] = {
            'message_hash': Variable(Type.bytes),
            'signature': Variable(Type.bytes),
        }

        super().__init__(identifier, syscall, args, return_type=Type.optional.build(Type.bytes))
