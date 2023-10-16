from boa3.internal.model.builtin.method import ScriptHashMethod
from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType
from boa3.internal.model.type.type import IType


class ECPointToScriptHashMethod(ScriptHashMethod):

    def __init__(self, data_type: IType = None):
        ec_point = ECPointType.build()
        if not ec_point.is_type_of(data_type):
            data_type = ec_point

        super().__init__(data_type)

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal import constants
        from boa3.internal.model.builtin.interop.crypto import CheckSigMethod
        from boa3.internal.model.builtin.interop.interop import Interop
        from boa3.internal.model.operation.binaryop import BinaryOp

        ecpoint_default = ECPointType.build().default_value

        # build CheckSig script
        from boa3.internal.neo.vm.opcode import OpcodeHelper
        push_ecpoint_opcode, push_ecpoint_data = OpcodeHelper.get_pushdata_and_data_from_size(len(ecpoint_default))
        code_generator.convert_literal(push_ecpoint_opcode + push_ecpoint_data)
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_literal(CheckSigMethod.get_raw_bytes())
        code_generator.convert_operation(BinaryOp.Concat, is_internal=True)
        code_generator.convert_operation(BinaryOp.Concat, is_internal=True)

        # to_script_hash
        code_generator.convert_builtin_method_call(Interop.Sha256, is_internal=True)
        code_generator.convert_builtin_method_call(Interop.Ripemd160, is_internal=True)

        # limit result to UInt160 length
        code_generator.convert_literal(0)
        code_generator.convert_literal(constants.SIZE_OF_INT160)
        code_generator.convert_get_substring(is_internal=True)
        code_generator.convert_cast(self.return_type, is_internal=True)
