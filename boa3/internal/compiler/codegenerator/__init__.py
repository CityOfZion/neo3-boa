from typing import List, Tuple

from boa3.internal.model.expression import IExpression
from boa3.internal.model.symbol import ISymbol
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer


def get_bytes(instructions: List[Tuple[Opcode, bytes]]) -> bytes:
    return b''.join([opcode + arg for opcode, arg in instructions])


def get_bytes_count(instructions: List[Tuple[Opcode, bytes]]) -> int:
    return sum([len(opcode) + len(arg) for opcode, arg in instructions])


def get_storage_key_for_variable(symbol: ISymbol) -> bytes:
    if isinstance(symbol, IExpression):
        symbol_obj = symbol.origin
    else:
        symbol_obj = symbol

    origin_hash = Integer(hash(symbol_obj)).to_byte_array()
    symbol_hash = Integer(hash(symbol)).to_byte_array()
    return Integer(hash(origin_hash + symbol_hash)).to_byte_array()
