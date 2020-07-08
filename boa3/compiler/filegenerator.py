import json
import logging
from typing import Any, Dict, List

from boa3.builtin import NeoMetadata
from boa3.constants import ENCODING
from boa3.model.method import Method
from boa3.model.symbol import ISymbol
from boa3.neo import to_hex_str
from boa3.neo.contracts.neffile import NefFile


class FileGenerator:
    """
    This class is responsible for generating the files.
    """

    def __init__(self, bytecode: bytes, metadata: NeoMetadata, symbols: Dict[str, ISymbol] = None):
        if symbols is None:
            symbols = {}
        self._metadata = metadata
        self._symbols: Dict[str, ISymbol] = symbols
        self._nef: NefFile = NefFile(bytecode)

    @property
    def _nef_hash(self) -> str:
        """
        Gets the string representation of the hash of the nef file

        :return: the hex string representation of the hash
        """
        return '0x' + to_hex_str(self._nef.script_hash)

    @property
    def _public_methods(self) -> Dict[str, Method]:
        """
        Gets a sublist of the symbols containing all public methods

        :return: a dictionary that maps each public method with its identifier
        """
        return {name: method for name, method in self._methods.items() if method.is_public}

    @property
    def _methods(self) -> Dict[str, Method]:
        """
        Gets a sublist of the symbols containing all user methods

        :return: a dictionary that maps each method with its identifier
        """
        from boa3.model.builtin.decorator.builtindecorator import IBuiltinDecorator
        return {name: method for name, method in self._symbols.items()
                if isinstance(method, Method) and not isinstance(method, IBuiltinDecorator)}

    def generate_nef_file(self) -> bytes:
        """
        Generates the .nef file

        :return: the resulting nef file as a byte array
        """
        return self._nef.serialize()

    def generate_manifest_file(self) -> bytes:
        """
        Generates the .manifest metadata file

        :return: the resulting manifest as a byte array
        """
        data: Dict[str, Any] = self._get_manifest_info()
        json_data: str = json.dumps(data, indent=4)
        return bytes(json_data, ENCODING)

    def _get_manifest_info(self) -> Dict[str, Any]:
        """
        Gets the manifest information in a dictionary format

        :return: a dictionary with the manifest information
        """
        # TODO: fill the information of the manifest
        return {
            "groups": [],
            "features": {
                "storage": self._metadata.has_storage,
                "payable": self._metadata.is_payable
            },
            "abi": self._get_abi_info(),
            "permissions": [
                {
                    "contract": "*",
                    "methods": "*"
                }
            ],
            "trusts": [],
            "safeMethods": [],
            "extra": self._metadata.extra if len(self._metadata.extra) > 0 else None
        }

    def generate_abi_file(self) -> bytes:
        """
        Generates the .abi metadata file

        :return: the resulting abi as a byte array
        """
        data: Dict[str, Any] = self._get_abi_info()
        json_data: str = json.dumps(data)
        return bytes(json_data, ENCODING)

    def _get_abi_info(self) -> Dict[str, Any]:
        """
        Gets the abi information in a dictionary format

        :return: a dictionary with the abi information
        """
        return {
            "hash": self._nef_hash,
            "methods": self._get_abi_methods(),
            "events": self._get_abi_events()
        }

    def _get_abi_methods(self) -> List[Dict[str, Any]]:
        """
        Gets the abi methods in a dictionary format

        :return: a dictionary with the abi methods
        """
        methods = []
        for method_id, method in self._public_methods.items():
            logging.info("'{0}' method included in the ABI".format(method_id))
            methods.append(self._construct_abi_method(method_id, method))
        return methods

    def _construct_abi_method(self, method_id: str, method: Method) -> Dict[str, Any]:
        return {
            "name": method_id,
            "offset": method.bytecode_address if method.bytecode_address is not None else 0,
            "parameters": [
                {
                    "name": arg_id,
                    "type": arg.type.abi_type
                } for arg_id, arg in method.args.items()
            ],
            "returnType": method.type.abi_type
        }

    def _get_abi_events(self) -> List[Dict[str, Any]]:
        """
        Gets the abi events in a dictionary format

        :return: a dictionary with the abi events
        """
        # TODO: abi events
        return []

    def generate_avmdbgnfo_file(self) -> bytes:
        """
        Generates a debug map for NEO debugger

        :return: the resulting map as a byte array
        """
        raise NotImplementedError
