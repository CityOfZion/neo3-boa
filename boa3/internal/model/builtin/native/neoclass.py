from typing import Any, Self

from boa3.internal.constants import NEO_SCRIPT
from boa3.internal.model.builtin.interop.contract import NeoToken
from boa3.internal.model.builtin.native.inativecontractclass import INativeContractClass
from boa3.internal.model.method import Method


class NeoClass(INativeContractClass):
    """
    A class used to represent NEO native contract
    """

    def __init__(self):
        super().__init__('NeoToken', NeoToken)

    @property
    def class_methods(self) -> dict[str, Method]:
        # avoid recursive import
        from boa3.internal.model.builtin.native.nep17_methods import (BalanceOfMethod, DecimalsMethod, SymbolMethod,
                                                                      TotalSupplyMethod, TransferMethod)
        from boa3.internal.model.builtin.native.neo_contract_methods import (
            GetAccountStateMethod, GetAllCandidatesMethod, GetCandidatesMethod, GetCandidateVoteMethod,
            GetCommitteeMethod, GetGasPerBlockMethod, GetNextBlockValidatorsMethod, GetRegisterPriceMethod,
            RegisterCandidateMethod, UnclaimedGasMethod, UnregisterCandidateMethod, UnVoteMethod, VoteMethod,
            GetCommitteeAddressMethod
        )
        from boa3.internal.model.builtin.contract import NeoAccountStateType

        if len(self._class_methods) == 0:
            self._class_methods = {
                'balanceOf': BalanceOfMethod(NEO_SCRIPT),
                'decimals': DecimalsMethod(NEO_SCRIPT),
                'symbol': SymbolMethod(NEO_SCRIPT),
                'totalSupply': TotalSupplyMethod(NEO_SCRIPT),
                'transfer': TransferMethod(NEO_SCRIPT),

                'get_account_state': GetAccountStateMethod(NeoAccountStateType.build()),
                'get_all_candidates': GetAllCandidatesMethod(),
                'get_candidates': GetCandidatesMethod(),
                'get_candidate_vote': GetCandidateVoteMethod(),
                'get_committee': GetCommitteeMethod(),
                'get_committee_address': GetCommitteeAddressMethod(),
                'get_gas_per_block': GetGasPerBlockMethod(),
                'get_next_block_validators': GetNextBlockValidatorsMethod(),
                'get_register_price': GetRegisterPriceMethod(),
                'register_candidate': RegisterCandidateMethod(),
                'unclaimed_gas': UnclaimedGasMethod(),
                'unregister_candidate': UnregisterCandidateMethod(),
                'un_vote': UnVoteMethod(),
                'vote': VoteMethod(),
            }
        return super().class_methods

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _Neo

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, NeoClass)


_Neo = NeoClass()
