from boa3.builtin.interop.runtime import check_witness


def Main(script_hash: list) -> bool:
    return check_witness(script_hash)
