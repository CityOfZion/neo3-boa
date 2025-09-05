from __future__ import annotations

__all__ = [
    'UInt160',
    'UInt256',
    'ECPoint',
    'Event',
    'Address',
    'BlockHash',
    'PublicKey',
    'ScriptHash',
    'ScriptHashLittleEndian',
    'TransactionId',
    'Block',
    "Signer",
    "WitnessRule",
    "WitnessCondition",
    "WitnessConditionType",
    "WitnessRuleAction",
    "WitnessScope",
    'Transaction',
    'Contract',
    'ContractManifest',
    'ContractPermission',
    'ContractPermissionDescriptor',
    'ContractGroup',
    'ContractAbi',
    'ContractMethodDescriptor',
    'ContractEventDescriptor',
    'ContractParameterDefinition',
    'ContractParameterType',
    'Nep17Contract',
    'Opcode',
    'FindOptions',
    'NamedCurveHash',
    'IBls12381',
    'Role',
    'Notification',
    'TriggerType',
    'VMState',
    'CallFlags',
    'OracleResponseCode',
    'NeoAccountState',
    'TransactionAttributeType',
]

from typing import Any

from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.ContractParameterType import ContractParameterType
from boa3.internal.neo3.contracts import CallFlags
from boa3.internal.neo3.contracts import TriggerType
from boa3.internal.neo3.contracts.findoptions import FindOptions
from boa3.internal.neo3.contracts.namedcurvehash import NamedCurveHash
from boa3.internal.neo3.contracts.native import Role
from boa3.internal.neo3.network.payloads import OracleResponseCode
from boa3.internal.neo3.network.payloads.transactionattributetype import TransactionAttributeType
from boa3.internal.neo3.network.payloads.verification import WitnessScope, WitnessRuleAction, WitnessConditionType
from boa3.internal.neo3.vm import VMState


class UInt160(bytes):
    """
    Represents a 160-bit unsigned integer.
    """
    zero: UInt160

    def __init__(self, arg: bytes | int = 0):
        super().__init__()
        pass


class UInt256(bytes):
    """
    Represents a 256-bit unsigned integer.
    """
    zero: UInt256

    def __init__(self, arg: bytes | int = 0):
        super().__init__()
        pass


class ECPoint(bytes):
    """
    Represents a coordinate pair for elliptic curve cryptography (ECC) structures.
    """
    zero: ECPoint

    def __init__(self, arg: bytes):
        super().__init__()
        pass

    def to_script_hash(self) -> UInt160:
        """
        Converts a data to a script hash.

        :return: the script hash of the data
        :rtype: bytes
        """
        pass


class Event:
    """
    Describes an action that happened in the blockchain.
    Neo3-Boa compiler won't recognize the `__init__` of this class. To create a new Event, use the method `CreateNewEvent`:

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/develop/write/basics#events>`__ to learn more
    about Events.

    >>> from boa3.sc.utils import CreateNewEvent
    ... new_event: Event = CreateNewEvent(  # create a new Event with the CreateNewEvent method
    ...     [
    ...        ('name', str),
    ...        ('amount', int)
    ...     ],
    ...     'New Event'
    ... )
    """

    def __call__(self, *args, **kwargs):
        pass


Address = str
"""
A type used only to indicate that a parameter or return on the manifest should be treated as an Address.
Same as str.

:meta hide-value:
"""


BlockHash = UInt256
"""
A type used only to indicate that a parameter or return on the manifest should be treated as a BlockHash.
Same as UInt256.

:meta hide-value:
"""


PublicKey = ECPoint
"""
A type used only to indicate that a parameter or return on the manifest should be treated as a PublicKey.
Same as ECPoint.

:meta hide-value:
"""


ScriptHash = UInt160
"""
A type used only to indicate that a parameter or return on the manifest should be treated as a ScriptHash.
Same as UInt160.

:meta hide-value:
"""


ScriptHashLittleEndian = UInt160
"""
A type used only to indicate that a parameter or return on the manifest should be treated as a
ScriptHashLittleEndian.
Same as UInt160.

:meta hide-value:
"""


TransactionId = UInt256
"""
A type used only to indicate that a parameter or return on the manifest should be treated as a TransactionId.
Same as UInt256.

:meta hide-value:
"""


class Block:
    """
    Represents a block.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/foundation/Blocks>`__ to learn more
    about Blocks.

    :ivar hash: a unique identifier based on the unsigned data portion of the object
    :vartype hash: boa3.sc.types.UInt256
    :ivar version: the data structure version of the block
    :vartype version: int
    :ivar previous_hash: the hash of the previous block
    :vartype previous_hash: boa3.sc.types.UInt256
    :ivar merkle_root: the merkle root of the transactions
    :vartype merkle_root: boa3.sc.types.UInt256
    :ivar timestamp: UTC timestamp of the block in milliseconds
    :vartype timestamp: int
    :ivar nonce: a random number used once in the cryptography
    :vartype nonce: int
    :ivar index: the index of the block
    :vartype index: int
    :ivar primary_index: the primary index of the consensus node that generated this block
    :vartype primary_index: int
    :ivar next_consensus: the script hash of the consensus nodes that generates the next block
    :vartype next_consensus: boa3.sc.types.UInt160
    :ivar transaction_count: the number of transactions on this block
    :vartype transaction_count: int
    """

    def __init__(self):
        self.hash: UInt256 = UInt256()
        self.version: int = 0
        self.previous_hash: UInt256 = UInt256()
        self.merkle_root: UInt256 = UInt256()
        self.timestamp: int = 0
        self.nonce: int = 0
        self.index: int = 0
        self.primary_index: int = 0
        self.next_consensus: UInt160 = UInt160()
        self.transaction_count: int = 0


class Contract:
    """
    Represents a contract that can be invoked.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/glossary#smart-contract>`__ to learn about
    Smart Contracts.

    :ivar id: the serial number of the contract
    :vartype id: int
    :ivar update_counter: the number of times the contract was updated
    :vartype update_counter: int
    :ivar hash: the hash of the contract
    :vartype hash: boa3.sc.types.UInt160
    :ivar nef: the serialized Neo Executable Format (NEF) object holding of the smart contract code and compiler
        information
    :vartype nef: bytes
    :ivar manifest: the manifest of the contract
    :vartype manifest: ContractManifest
    """

    def __init__(self):
        self.id: int = 0
        self.update_counter: int = 0
        self.hash: UInt160 = UInt160()
        self.nef: bytes = bytes()
        self.manifest: ContractManifest = ContractManifest()


class ContractManifest:
    """
    Represents the manifest of a smart contract.

    When a smart contract is deployed, it must explicitly declare the features and permissions it will use.

    When it is running, it will be limited by its declared list of features and permissions, and cannot make any
    behavior beyond the scope of the list.

    For more details, check out `NEP-15 <https://github.com/neo-project/proposals/blob/master/nep-15.mediawiki>`__ or
    `Neo's Documentation <https://developers.neo.org/docs/n3/develop/write/manifest#manifest>`__.

    :ivar name: The name of the contract.
    :vartype name: str
    :ivar groups: The groups of the contract.
    :vartype groups: list[ContractGroup]
    :ivar supported_standards: Indicates which standards the contract supports. It can be a list of NEPs.
    :vartype supported_standards: list[str]
    :ivar abi: The ABI of the contract.
    :vartype abi: ContractAbi
    :ivar permissions: The permissions of the contract.
    :vartype permissions: list[ContractPermission]
    :ivar trusts:
        The trusted contracts and groups of the contract.

        If a contract is trusted, the user interface will not give any warnings when called by the contract.

    :vartype trusts: list[ContractPermissionDescriptor] or None
    :ivar extras: Custom user data as a json string.
    :vartype extras: str
    """

    def __init__(self):
        self.name: str = ''
        self.groups: list[ContractGroup] = []
        self.supported_standards: list[str] = []
        self.abi: ContractAbi = None
        self.permissions: list[ContractPermission] = []
        self.trusts: list[ContractPermissionDescriptor] | None = None
        self.extras: str = ''


class ContractPermission:
    """
    Represents a permission of a contract. It describes which contracts may be invoked and which methods are called.

    If a contract invokes a contract or method that is not declared in the manifest at runtime, the invocation will
    fail.

    :ivar contract:
        Indicates which contract to be invoked.

        It can be a hash of a contract, a public key of a group, or a wildcard \\*.

        If it specifies a hash of a contract, then the contract will be invoked; If it specifies a public key of a
        group, then any contract in this group may be invoked; If it specifies a wildcard \\*, then any contract may be
        invoked.

    :vartype contract: ContractPermissionDescriptor or None
    :ivar methods:
        Indicates which methods to be called.

        It can also be assigned with a wildcard \\*. If it is a wildcard \\*, then it means that any method can be
        called.

    :vartype methods: list[str] or None
    """

    def __init__(self):
        self.contract: ContractPermissionDescriptor | None = None
        self.methods: list[str] | None = None


class ContractPermissionDescriptor:
    """
    Indicates which contracts are authorized to be called.

    :ivar hash: The hash of the contract.
    :vartype hash: boa3.sc.types.UInt160 or None
    :ivar group: The group of the contracts.
    :vartype group: boa3.sc.types.ECPoint or None
    """

    def __init__(self):
        self.hash: UInt160 | None = None
        self.group: ECPoint | None = None


class ContractGroup:
    """
    Represents a set of mutually trusted contracts.

    A contract will trust and allow any contract in the same group to invoke it, and the user interface will not give
    any warnings.

    A group is identified by a public key and must be accompanied by a signature for the contract hash to prove that
    the contract is indeed included in the group.

    :ivar pubkey: The public key of the group.
    :vartype pubkey: boa3.sc.types.ECPoint
    :ivar signature: The signature of the contract hash which can be verified by `pubkey`.
    :vartype signature: bytes
    """

    def __init__(self):
        self.pubkey: ECPoint = ECPoint(b'')
        self.signature: bytes = b''


class ContractAbi:
    """
    Represents the ABI of a smart contract.

    For more details, check out `NEP-14 <https://github.com/neo-project/proposals/blob/master/nep-14.mediawiki>`__ or
    `Neo's Documentation <https://developers.neo.org/docs/n3/develop/write/manifest#manifest>`__.

    :ivar methods: Gets the methods in the ABI.
    :vartype methods: list[ContractMethodDescriptor]
    :ivar events: Gets the events in the ABI.
    :vartype events: list[ContractEventDescriptor]
    """

    def __init__(self):
        self.methods: list[ContractMethodDescriptor] = []
        self.events: list[ContractEventDescriptor] = []


class ContractMethodDescriptor:
    """
    Represents a method in a smart contract ABI.

    :ivar name: The name of the method.
    :vartype name: str
    :ivar parameters: The parameters of the method.
    :vartype parameters: list[ContractParameterDefinition]
    :ivar return_type: Indicates the return type of the method.
    :vartype return_type: ContractParameterType
    :ivar offset: The position of the method in the contract script.
    :vartype offset: int
    :ivar safe:
        Indicates whether the method is a safe method.

        If a method is marked as safe, the user interface will not give any warnings when it is called by other
        contracts.

    :vartype safe: bool
    """

    def __init__(self):
        self.name: str = ''
        self.parameters: list[ContractParameterDefinition] = []
        self.return_type: ContractParameterType = ContractParameterType.Any
        self.offset: int = 0
        self.safe: bool = False


class ContractEventDescriptor:
    """
    Represents an event in a smart contract ABI.

    :ivar name: The name of the event.
    :vartype name: str
    :ivar parameters: The parameters of the event.
    :vartype parameters: list[ContractParameterDefinition]
    """

    def __init__(self):
        self.name: str = ''
        self.parameters: list[ContractParameterDefinition] = []


class ContractParameterDefinition:
    """
    Represents a parameter of an event or method in ABI.

    :ivar name: The name of the parameter.
    :vartype name: str
    :ivar type: The type of the parameter.
    :vartype type: ContractParameterType
    """

    def __init__(self):
        self.name: str = ''
        self.type: ContractParameterType = ContractParameterType.Any


class Nep17Contract(Contract):
    def symbol(self) -> str:
        pass

    def decimals(self) -> int:
        pass

    def total_supply(self) -> int:
        pass

    def balance_of(self, account: UInt160) -> int:
        pass

    def transfer(self, from_address: UInt160, to_address: UInt160, amount: int, data: Any = None) -> bool:
        pass


class Signer:
    """
    Represents a signer.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/foundation/Transactions#signers>`__ to learn more
    about Signers.

    :ivar account:
    :vartype account: boa3.sc.types.UInt160
    :ivar scopes:
    :vartype scopes: WitnessScope
    :ivar allowed_contracts:
    :vartype allowed_contracts: list[boa3.sc.types.UInt160]
    :ivar allowed_groups:
    :vartype allowed_groups: list[boa3.sc.types.UInt160]
    :ivar rules:
    :vartype rules: list[WitnessRule]
    """

    def __init__(self):
        self.account: UInt160 = UInt160()
        self.scopes: WitnessScope = WitnessScope.NONE
        self.allowed_contracts: list[UInt160] = []
        self.allowed_groups: list[UInt160] = []
        self.rules: list[WitnessRule] = []


class WitnessRule:
    """
    Represents a witness rule.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/foundation/Transactions#witnessrule>`__ to learn
    more about WitnessRules.

    :ivar action:
    :vartype action: WitnessRuleAction
    :ivar condition:
    :vartype condition: WitnessCondition
    """

    def __init__(self):
        self.action: WitnessRuleAction = WitnessRuleAction.DENY
        self.condition: WitnessCondition = WitnessCondition()


class WitnessCondition:
    """
    Represents a witness condition.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/foundation/Transactions#witnesscondition>`__ to
    learn more about WitnessConditions.

    :ivar type:
    :vartype type: WitnessConditionType
    """

    def __init__(self):
        self.type: WitnessConditionType = WitnessConditionType.BOOLEAN


class Transaction:
    """
    Represents a transaction.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/foundation/Transactions>`__ to learn more about
    Transactions.

    :ivar hash: a unique identifier based on the unsigned data portion of the object
    :vartype hash: boa3.sc.types.UInt256
    :ivar version: the data structure version of the transaction
    :vartype version: int
    :ivar nonce: a random number used once in the cryptography
    :vartype nonce: int
    :ivar sender: the sender is the first signer of the transaction, they will pay the fees of the transaction
    :vartype sender: boa3.sc.types.UInt160
    :ivar system_fee: the fee paid for executing the `script`
    :vartype system_fee: int
    :ivar network_fee: the fee paid for the validation and inclusion of the transaction in a block by the consensus node
    :vartype network_fee: int
    :ivar valid_until_block: indicates that the transaction is only valid before this block height
    :vartype valid_until_block: int
    :ivar script: the array of instructions to be executed on the transaction chain by the virtual machine
    :vartype script: bytes
    """

    def __init__(self):
        self.hash: UInt256 = UInt256()
        self.version: int = 0
        self.nonce: int = 0
        self.sender: UInt160 = UInt160()
        self.system_fee: int = 0
        self.network_fee: int = 0
        self.valid_until_block: int = 0
        self.script: bytes = b''


class IBls12381:

    def __init__(self):
        pass


class Notification:
    """
    Represents a notification.

    :ivar script_hash: the script hash of the notification sender
    :vartype script_hash: boa3.sc.types.UInt160
    :ivar event_name: the notification's name
    :vartype event_name: str
    :ivar state: a tuple value storing all the notification contents.
    :vartype state: tuple
    """

    def __init__(self):
        self.script_hash: UInt160 = UInt160()
        self.event_name: str = ''
        self.state: tuple = ()


class NeoAccountState:
    """
    Represents the account state of NEO token in the NEO system.

    :ivar balance: the current account balance, which equals to the votes cast
    :vartype balance: int
    :ivar height: the height of the block where the balance changed last time
    :vartype height: int
    :ivar vote_to: the voting target of the account
    :vartype vote_to: boa3.sc.types.ECPoint
    """

    def __init__(self):
        from boa3.internal import constants
        self.balance: int = 0
        self.height: int = 0
        self.vote_to: ECPoint = ECPoint(bytes(constants.SIZE_OF_ECPOINT))
        self.last_gas_per_vote: int = 0
