from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.storage import try_get, try_get_bool, try_get_dict, try_get_list, try_get_str, try_get_int, \
    try_get_ecpoint, try_get_uint160, try_get_uint256, \
    try_get_object, get_context, put
from boa3.sc.types import ECPoint, UInt160, UInt256


@public
def _deploy(data: Any, update: bool):
    put(b'data1', b"fizz")
    put(b'data2', b"buzz")


@public
def try_get_bytes_local(key: bytes) -> tuple[bytes, bool]:
    return try_get(key)


@public
def try_get_bytes_context(key: bytes) -> tuple[bytes, bool]:
    return try_get(key, get_context().as_read_only())


@public
def try_get_bool_local(key: bytes) -> tuple[bool, bool]:
    return try_get_bool(key)


@public
def try_get_bool_context(key: bytes) -> tuple[bool, bool]:
    return try_get_bool(key, get_context().as_read_only())


@public
def try_get_dict_local(key: bytes) -> tuple[dict, bool]:
    return try_get_dict(key)


@public
def try_get_dict_context(key: bytes) -> tuple[dict, bool]:
    return try_get_dict(key, get_context().as_read_only())


@public
def try_get_list_local(key: bytes) -> tuple[list, bool]:
    return try_get_list(key)


@public
def try_get_list_context(key: bytes) -> tuple[list, bool]:
    return try_get_list(key, get_context().as_read_only())


@public
def try_get_str_local(key: bytes) -> tuple[str, bool]:
    return try_get_str(key)


@public
def try_get_str_context(key: bytes) -> tuple[str, bool]:
    return try_get_str(key, get_context().as_read_only())


@public
def try_get_int_local(key: bytes) -> tuple[int, bool]:
    return try_get_int(key)


@public
def try_get_int_context(key: bytes) -> tuple[int, bool]:
    return try_get_int(key, get_context().as_read_only())


@public
def try_get_ecpoint_local(key: bytes) -> tuple[ECPoint, bool]:
    return try_get_ecpoint(key)


@public
def try_get_ecpoint_context(key: bytes) -> tuple[ECPoint, bool]:
    return try_get_ecpoint(key, get_context().as_read_only())


@public
def try_get_uint160_local(key: bytes) -> tuple[UInt160, bool]:
    return try_get_uint160(key)


@public
def try_get_uint160_context(key: bytes) -> tuple[UInt160, bool]:
    return try_get_uint160(key, get_context().as_read_only())


@public
def try_get_uint256_local(key: bytes) -> tuple[UInt256, bool]:
    return try_get_uint256(key)


@public
def try_get_uint256_context(key: bytes) -> tuple[UInt256, bool]:
    return try_get_uint256(key, get_context().as_read_only())


@public
def try_get_object_local(key: bytes) -> tuple[Any, bool]:
    return try_get_object(key)


@public
def try_get_object_context(key: bytes) -> tuple[Any, bool]:
    return try_get_object(key, get_context().as_read_only())
