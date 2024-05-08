from typing import TypeVar, cast

from neo3.core import types
from neo3.core.cryptography import ECPoint

JsonToken = int | str | bool | None | list['JsonToken'] | dict[str, 'JsonToken']
JsonObject = dict[str, JsonToken]

NotificationState = TypeVar('NotificationState', list, tuple)
Notification = tuple[
    types.UInt160,  # contract
    str,  # notification name
    NotificationState  # state
]

Transaction = tuple[
    types.UInt256,  # hash
    int,  # version
    int,  # nonce
    types.UInt160,  # sender
    int,  # system fee
    int,  # network fee
    int,  # valid until block
    bytes,  # script
]

Block = tuple[
    types.UInt256,  # hash
    int,    # version
    types.UInt256,  # previous hash
    types.UInt256,  # merkle root
    int,  # timestamp
    int,  # nonce
    int,  # index
    types.UInt160,  # next consensus
    int,  # tx count
]

Signer = tuple[
    types.UInt160,  # account
    int,  # witness scope type
    types.UInt160,  # allowed contracts
    types.UInt160,  # allowed groups
    list[tuple[int, tuple[int]]],  # rules
]

ContractParameterType = int
ContractMethod = tuple[
    str,  # name
    list[tuple[str, ContractParameterType]],
    ContractParameterType,  # return type
    int,  # offset
    bool  # safe
]
ContractEvent = tuple[
    str,  # name
    list[tuple[str, ContractParameterType]]
]
ContractAbi = tuple[
    list[ContractMethod],
    list[ContractEvent]
]
ContractManifest = tuple[
    str,  # name
    list,  # groups
    dict,  # features
    list,  # supported standards
    ContractAbi,
    list,  # permissions
    list,  # trusts
    str  # extra
]
Contract = tuple[
    int,  # contract id
    int,  # update counter
    types.UInt160,  # contract hash
    bytes,  # contract nef
    ContractManifest  # contract manifest
]

NeoAccountState = tuple[
    int,  # balance
    int,  # height
    ECPoint,  # vote to
    int,  # last gas per vote
]


def manifest_from_json(json_: JsonObject) -> ContractManifest:
    import json
    from boa3.internal.neo.vm.type.ContractParameterType import ContractParameterType

    name = json_['name']
    groups = json_['groups'] if 'groups' in json_ else []
    supported_standards = json_['supportedstandards'] if 'supportedstandards' in json_ else []
    permissions = json_['permissions'] if 'permissions' in json_ else []
    trusts = json_['trusts'] if 'trusts' in json_ else []
    extra = json.dumps(json_['extra'], separators=(',', ':'))

    json_methods, json_events = json_['abi'].values()
    methods: list[ContractMethod] = [
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
    events: list[ContractEvent] = [
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
