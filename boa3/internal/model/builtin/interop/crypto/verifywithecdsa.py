from boa3.internal.model.builtin.interop.nativecontract import CryptoLibMethod
from boa3.internal.model.variable import Variable


class VerifyWithECDsaMethod(CryptoLibMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType
        from boa3.internal.model.builtin.interop.crypto.namedcurvetype import NamedCurveType

        identifier = 'verify_with_ecdsa'
        native_identifier = 'verifyWithECDsa'
        args: dict[str, Variable] = {
            'data': Variable(Type.bytes),
            'pubkey': Variable(ECPointType.build()),
            'signature': Variable(Type.bytes),
            'curve': Variable(NamedCurveType.build())
        }
        super().__init__(identifier, native_identifier, args, return_type=Type.bool)
