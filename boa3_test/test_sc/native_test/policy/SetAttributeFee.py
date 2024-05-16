from boa3.sc.compiletime import public
from boa3.sc.contracts import PolicyContract
from boa3.sc.types import TransactionAttributeType


@public
def main(tx_att: TransactionAttributeType, value: int):
    PolicyContract.set_attribute_fee(tx_att, value)


@public
def get_tx_attr(tx_att: TransactionAttributeType) -> int:
    return PolicyContract.get_attribute_fee(tx_att)
