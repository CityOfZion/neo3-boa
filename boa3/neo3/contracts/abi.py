from __future__ import annotations

import warnings
from enum import IntEnum
from typing import List

from boa3.neo3 import contracts
from boa3.neo3.core import types, IJson


class ContractParameterType(IntEnum):
    SIGNATURE = 0x00,
    BOOLEAN = 0x01,
    INTEGER = 0x02,
    HASH160 = 0x03,
    HASH256 = 0x04,
    BYTEARRAY = 0x05,
    PUBLICKEY = 0x06,
    STRING = 0x07,
    ARRAY = 0x10,
    MAP = 0x12,
    INTEROP_INTERFACE = 0xf0,
    ANY = 0xfe,
    VOID = 0xff


class ContractParameterDefinition(IJson):
    """
    A parameter description for a contract Method or Event.
    """

    def __init__(self, name: str, type: contracts.ContractParameterType):
        """
        Args:
            name: the human readable identifier.
            type: the type of parameter.
        """
        self.name = name
        self.type = type

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.name == other.name and self.type == other.type

    def to_json(self) -> dict:
        """
        Convert object into JSON representation.
        """
        json = {
            "name": self.name,
            "type": self.type.name.title()
        }
        return json

    @classmethod
    def from_json(cls, json: dict) -> ContractParameterDefinition:
        """
        Parse object out of JSON data.

        Args:
            json: a dictionary.

        Raises:
            KeyError: if the data supplied does not contain the necessary keys.
        """
        return cls(
            name=json['name'],
            type=contracts.ContractParameterType[json['type'].upper()]
        )


class ContractEventDescriptor(IJson):
    """
    A description for an event that a contract can broadcast.
    """

    def __init__(self, name: str, parameters: List[ContractParameterDefinition]):
        """

        Args:
            name: the human readable identifier of the event.
            parameters: the list of parameters the event takes.
        """
        self.name = name
        self.parameters = parameters

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.name == other.name and self.parameters == other.parameters

    def to_json(self) -> dict:
        """
        Convert object into JSON representation.
        """
        json = {
            "name": self.name,
            "parameters": list(map(lambda p: p.to_json(), self.parameters))
        }
        return json

    @classmethod
    def from_json(cls, json: dict) -> ContractEventDescriptor:
        """
        Parse object out of JSON data.

        Args:
            json: a dictionary.

        Raises:
            KeyError: if the data supplied does not contain the necessary key.
        """
        return cls(
            name=json['name'],
            parameters=list(map(lambda p: ContractParameterDefinition.from_json(p), json['parameters']))
        )


class ContractMethodDescriptor(ContractEventDescriptor, IJson):
    """
    A description of a callable method on a contract.
    """

    def __init__(self, name: str,
                 parameters: List[ContractParameterDefinition],
                 return_type: contracts.ContractParameterType):
        """
        Args:
            name: the human readable identifier of the method.
            parameters: the list of parameters the method takes.
            return_type: the type of the returned value.
        """
        super(ContractMethodDescriptor, self).__init__(name, parameters)
        self.return_type = return_type

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return (self.name == other.name
                and self.parameters == other.parameters
                and self.return_type == other.return_type)

    @classmethod
    def default_entrypoint(cls) -> ContractMethodDescriptor:
        """
        Create an entry point accepting an operation and a list of arguments.

        Note: deprecated post neo3-preview2.
        """
        warnings.warn("Will be deprecated post neo3-preview2", PendingDeprecationWarning)
        return cls(
            "Main",
            [
                ContractParameterDefinition("operation", contracts.ContractParameterType.STRING),
                ContractParameterDefinition("args", contracts.ContractParameterType.ARRAY)
            ],
            contracts.ContractParameterType.ANY
        )

    def to_json(self) -> dict:
        """
        Convert object into JSON representation.
        """
        json = super(ContractMethodDescriptor, self).to_json()
        json.update({
            "returnType": self.return_type.name.title()
        })
        return json

    @classmethod
    def from_json(cls, json: dict) -> ContractMethodDescriptor:
        """
        Parse object out of JSON data.

        Args:
            json: a dictionary.

        Raises:
            KeyError: if the data supplied does not contain the necessary keys.
        """
        return cls(
            name=json['name'],
            parameters=list(map(lambda p: contracts.ContractParameterDefinition.from_json(p), json['parameters'])),
            return_type=contracts.ContractParameterType[json['returnType'].upper()]
        )


class ContractABI(IJson):
    """
    The smart contract application binary interface describes the callable events and contracts for a given
    smart contract.
    """

    def __init__(self,
                 contract_hash: types.UInt160,
                 entry_point: contracts.ContractMethodDescriptor,
                 methods: List[contracts.ContractMethodDescriptor],
                 events: List[contracts.ContractEventDescriptor]):
        """

        Args:
            contract_hash: the result of performing RIPEMD160(SHA256(vm_script)), where vm_script is the smart contract
            byte code.
            entry_point: Obsolete after preview 2.
            methods: the available methods in the contract.
            events: the various events that can be broad casted by the contract.
        """
        self.contract_hash = contract_hash
        self.entry_point = entry_point
        self.methods = methods
        self.events = events

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return (self.contract_hash == other.contract_hash
                and self.entry_point == other.entry_point
                and self.methods == other.methods
                and self.events == other.events)

    def to_json(self) -> dict:
        """
        Convert object into JSON representation.
        """
        json = {
            "hash": '0x' + str(self.contract_hash),
            "entryPoint": self.entry_point.to_json(),
            "methods": list(map(lambda m: m.to_json(), self.methods)),
            "events": list(map(lambda e: e.to_json(), self.events))
        }
        return json

    @classmethod
    def from_json(cls, json: dict) -> ContractABI:
        """
        Parse object out of JSON data.

        Args:
            json: a dictionary.

        Raises:
            KeyError: if the data supplied does not contain the necessary keys.
        """
        return cls(
            contract_hash=types.UInt160.from_string(json['hash'][2:]),
            entry_point=contracts.ContractMethodDescriptor.from_json(json['entryPoint']),
            methods=list(map(lambda m: contracts.ContractMethodDescriptor.from_json(m), json['methods'])),
            events=list(map(lambda e: contracts.ContractEventDescriptor.from_json(e), json['events'])),
        )
