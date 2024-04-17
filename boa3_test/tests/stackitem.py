from typing import Any, Protocol, TypeVar, cast

from neo3.core import types, cryptography
from neo3.network.payloads import block, transaction, verification

from boa3_test.tests import annotation

StackItem = TypeVar(
    'StackItem',
    int,
    bool,
    str,
    bytes,
    types.UInt160,
    types.UInt256,
    cryptography.ECPoint,
    tuple,
    list,
    dict,
    None
)


class StackItemProcessor(Protocol):
    def __call__(self, data: Any) -> StackItem:
        ...


def from_block(block_: block.Block) -> annotation.Block:
    return (
        block_.hash(),
        block_.version,
        block_.prev_hash,
        block_.merkle_root,
        block_.timestamp,
        block_.nonce,
        block_.index,
        block_.next_consensus,
        len(block_.transactions)
    )


def from_transaction(tx: transaction.Transaction) -> annotation.Transaction:
    return (
        tx.hash(),
        tx.version,
        tx.nonce,
        tx.sender,
        tx.system_fee,
        tx.network_fee,
        tx.valid_until_block,
        tx.script
    )


def from_signer(signer: verification.Signer) -> annotation.Signer:
    return (
        signer.account,
        int(signer.scope),
        signer.allowed_contracts,
        signer.allowed_groups,
        [(
            int(rule.action),
            (int(rule.condition.type),)
        ) for rule in signer.rules]
    )


def from_manifest(json_: annotation.JsonObject) -> annotation.ContractManifest:
    import json
    from boa3.internal.neo.vm.type.ContractParameterType import ContractParameterType

    name = json_['name']
    groups = json_['groups'] if 'groups' in json_ else []
    supported_standards = json_['supportedstandards'] if 'supportedstandards' in json_ else []
    permissions = json_['permissions'] if 'permissions' in json_ else []
    trusts = json_['trusts'] if 'trusts' in json_ else []
    extra = json.dumps(json_['extra'], separators=(',', ':'))

    json_methods, json_events = json_['abi'].values()
    methods: list[annotation.ContractMethod] = [
        (
            cast(str, method['name']),
            [(
                cast(str, param['name']),
                ContractParameterType._get_by_name(param['type'])
            ) for param in method['parameters']],
            ContractParameterType._get_by_name(method['returntype']),
            cast(int, method['offset']),
            cast(bool, method['safe'])
        ) for method in json_methods
    ]
    events: list[annotation.ContractEvent] = [
        (
            cast(str, event['name']),
            [(
                cast(str, param['name']),
                ContractParameterType._get_by_name(param['type'])
            ) for param in event['parameters']]
        ) for event in json_events
    ]

    return (
        name,
        groups,
        {},
        supported_standards,
        (methods, events),
        permissions,
        trusts,
        extra
    )
