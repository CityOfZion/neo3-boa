__all__ = [
    'ContractManifest',
    'ContractPermission',
    'ContractPermissionDescriptor',
    'ContractGroup',
    'ContractAbi',
    'ContractMethodDescriptor',
    'ContractEventDescriptor',
    'ContractParameterDefinition',
    'ContractParameterType',
]

from typing import List, Optional

from boa3.builtin.type import ECPoint, UInt160
from boa3.internal.neo.vm.type.ContractParameterType import ContractParameterType


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
    :vartype groups: List[ContractGroup]
    :ivar supported_standards: Indicates which standards the contract supports. It can be a list of NEPs.
    :vartype supported_standards: List[str]
    :ivar abi: The ABI of the contract.
    :vartype abi: ContractAbi
    :ivar permissions: The permissions of the contract.
    :vartype permissions: List[ContractPermission]
    :ivar trusts:
        The trusted contracts and groups of the contract.

        If a contract is trusted, the user interface will not give any warnings when called by the contract.

    :vartype trusts: List[ContractPermissionDescriptor] or None
    :ivar extras: Custom user data as a json string.
    :vartype extras: str
    """

    def __init__(self):
        self.name: str = ''
        self.groups: List[ContractGroup] = []
        self.supported_standards: List[str] = []
        self.abi: ContractAbi = None
        self.permissions: List[ContractPermission] = []
        self.trusts: Optional[List[ContractPermissionDescriptor]] = None
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

    :vartype methods: List[str] or None
    """

    def __init__(self):
        self.contract: Optional[ContractPermissionDescriptor] = None
        self.methods: Optional[List[str]] = None


class ContractPermissionDescriptor:
    """
    Indicates which contracts are authorized to be called.

    :ivar hash: The hash of the contract.
    :vartype hash: UInt160 or None
    :ivar group: The group of the contracts.
    :vartype group: ECPoint or None
    """

    def __init__(self):
        self.hash: Optional[UInt160] = None
        self.group: Optional[ECPoint] = None


class ContractGroup:
    """
    Represents a set of mutually trusted contracts.

    A contract will trust and allow any contract in the same group to invoke it, and the user interface will not give
    any warnings.

    A group is identified by a public key and must be accompanied by a signature for the contract hash to prove that
    the contract is indeed included in the group.

    :ivar pubkey: The public key of the group.
    :vartype pubkey: ECPoint
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
    :vartype methods: List[ContractMethodDescriptor]
    :ivar events: Gets the events in the ABI.
    :vartype events: List[ContractEventDescriptor]
    """

    def __init__(self):
        self.methods: List[ContractMethodDescriptor] = []
        self.events: List[ContractEventDescriptor] = []


class ContractMethodDescriptor:
    """
    Represents a method in a smart contract ABI.

    :ivar name: The name of the method.
    :vartype name: str
    :ivar parameters: The parameters of the method.
    :vartype parameters: List[ContractParameterDefinition]
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
        self.parameters: List[ContractParameterDefinition] = []
        self.return_type: ContractParameterType = ContractParameterType.Any
        self.offset: int = 0
        self.safe: bool = False


class ContractEventDescriptor:
    """
    Represents an event in a smart contract ABI.

    :ivar name: The name of the event.
    :vartype name: str
    :ivar parameters: The parameters of the event.
    :vartype parameters: List[ContractParameterDefinition]
    """

    def __init__(self):
        self.name: str = ''
        self.parameters: List[ContractParameterDefinition] = []


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
