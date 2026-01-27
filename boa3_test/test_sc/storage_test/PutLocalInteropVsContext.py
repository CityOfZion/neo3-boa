from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.storage import get, put, put_bool, put_dict, put_list, put_str, put_int, put_ecpoint, put_uint160, \
    put_uint256, put_object, get_context
from boa3.sc.types import ECPoint, UInt160, UInt256


@public
def get_value(key: bytes) -> bytes:
    return get(key)


@public
def put_bytes_local(key: bytes, value: bytes) -> None:
    return put(key, value)


@public
def put_bytes_context(key: bytes, value: bytes) -> None:
    return put(key, value, get_context())


@public
def put_bool_local(key: bytes, value: bool) -> None:
    return put_bool(key, value)


@public
def put_bool_context(key: bytes, value: bool) -> None:
    return put_bool(key, value, get_context())


@public
def put_dict_local(key: bytes, value: dict) -> None:
    return put_dict(key, value)


@public
def put_dict_context(key: bytes, value: dict) -> None:
    return put_dict(key, value, get_context())


@public
def put_list_local(key: bytes, value: list) -> None:
    return put_list(key, value)


@public
def put_list_context(key: bytes, value: list) -> None:
    return put_list(key, value, get_context())


@public
def put_str_local(key: bytes, value: str) -> None:
    return put_str(key, value)


@public
def put_str_context(key: bytes, value: str) -> None:
    return put_str(key, value, get_context())


@public
def put_int_local(key: bytes, value: int) -> None:
    return put_int(key, value)


@public
def put_int_context(key: bytes, value: int) -> None:
    return put_int(key, value, get_context())


@public
def put_ecpoint_local(key: bytes, value: ECPoint) -> None:
    return put_ecpoint(key, value)


@public
def put_ecpoint_context(key: bytes, value: ECPoint) -> None:
    return put_ecpoint(key, value, get_context())


@public
def put_uint160_local(key: bytes, value: UInt160) -> None:
    return put_uint160(key, value)


@public
def put_uint160_context(key: bytes, value: UInt160) -> None:
    return put_uint160(key, value, get_context())


@public
def put_uint256_local(key: bytes, value: UInt256) -> None:
    return put_uint256(key, value)


@public
def put_uint256_context(key: bytes, value: UInt256) -> None:
    return put_uint256(key, value, get_context())


@public
def put_object_local(key: bytes, value: Any) -> None:
    return put_object(key, value)


@public
def put_object_context(key: bytes, value: Any) -> None:
    return put_object(key, value, get_context())
