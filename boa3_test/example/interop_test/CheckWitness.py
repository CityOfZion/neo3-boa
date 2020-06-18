from boa3.interop.runtime import check_witness


def Main(script_hash: bytes) -> bool:
    return check_witness(script_hash)
