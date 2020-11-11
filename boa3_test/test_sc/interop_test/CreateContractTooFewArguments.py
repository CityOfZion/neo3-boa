from boa3.builtin.interop.contract import create_contract


def Main(scripthash: bytes):
    create_contract(scripthash)
