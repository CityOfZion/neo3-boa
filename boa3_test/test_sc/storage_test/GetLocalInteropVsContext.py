from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.storage import get, get_bool, get_dict, get_list, get_str, get_int, get_ecpoint, get_uint160, get_uint256, \
    get_object, get_context, put
from boa3.sc.types import ECPoint, UInt160, UInt256


@public
def _deploy(data: Any, update: bool):
    put(b'data1', b"fizz")
    put(b'data2', b"buzz")

@public
def get_bytes_local(key: bytes) -> bytes:
    return get(key)

@public
def get_bytes_context(key: bytes) -> bytes:
    return get(key, get_context().as_read_only())


# the methods below don't necessarily produce a valid output, they are just to test the opcodes generated
@public
def get_bool_local(key: bytes) -> bool:
    return get_bool(key)


@public
def get_bool_context(key: bytes) -> bool:
    return get_bool(key, get_context().as_read_only())


@public
def get_dict_local(key: bytes) -> dict:
    return get_dict(key)


@public
def get_dict_context(key: bytes) -> dict:
    return get_dict(key, get_context().as_read_only())


@public
def get_list_local(key: bytes) -> list:
    return get_list(key)


@public
def get_list_context(key: bytes) -> list:
    return get_list(key, get_context().as_read_only())


@public
def get_str_local(key: bytes) -> str:
    return get_str(key)


@public
def get_str_context(key: bytes) -> str:
    return get_str(key, get_context().as_read_only())


@public
def get_int_local(key: bytes) -> int:
    return get_int(key)


@public
def get_int_context(key: bytes) -> int:
    return get_int(key, get_context().as_read_only())


@public
def get_ecpoint_local(key: bytes) -> ECPoint:
    return get_ecpoint(key)


@public
def get_ecpoint_context(key: bytes) -> ECPoint:
    return get_ecpoint(key, get_context().as_read_only())


@public
def get_uint160_local(key: bytes) -> UInt160:
    return get_uint160(key)


@public
def get_uint160_context(key: bytes) -> UInt160:
    return get_uint160(key, get_context().as_read_only())


@public
def get_uint256_local(key: bytes) -> UInt256:
    return get_uint256(key)


@public
def get_uint256_context(key: bytes) -> UInt256:
    return get_uint256(key, get_context().as_read_only())


@public
def get_object_local(key: bytes) -> Any:
    return get_object(key)


@public
def get_object_context(key: bytes) -> Any:
    return get_object(key, get_context().as_read_only())
