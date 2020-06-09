import json
import logging
import sys
from typing import Any, Dict, List, Optional, Tuple

from boa3.model.method import Method
from boa3.model.symbol import ISymbol
from boa3.neo import to_hex_str
from boa3.neo.smart_contract.neffile import NefFile


class FileGenerator:
    """
    This class is responsible for generating the files.
    """

    def __init__(self, bytecode: bytes, symbols: Dict[str, ISymbol] = None):
        if symbols is None:
            symbols = {}
        self.__symbols: Dict[str, ISymbol] = symbols
        self.__nef: NefFile = NefFile(bytecode)

    @property
    def __nef_hash(self) -> str:
        """
        Gets the string representation of the hash of the nef file

        :return: the hex string representation of the hash
        """
        return '0x' + to_hex_str(self.__nef.script_hash)

    @property
    def __methods(self) -> Dict[str, Method]:
        """
        Gets a sublist of the symbols containing all the methods

        :return: a dictionary that maps each method with its identifier
        """
        return {name: method for name, method in self.__symbols.items() if isinstance(method, Method) and method.is_public}

    @property
    def __entry_point(self) -> Optional[Tuple[str, Method]]:
        """
        Gets the entry point method of the smart contract

        :return: a tuple with the name and the method if found. Otherwise, return None
        :rtype: Tuple[str, Method] or None
        """
        method_id = None
        if 'main' in self.__methods:
            method_id = 'main'
        elif 'Main' in self.__methods:
            method_id = 'Main'

        if method_id is None:
            raise NotImplementedError
        else:
            return method_id, self.__methods[method_id]

    def generate_nef_file(self) -> bytes:
        """
        Generates the .nef file

        :return: the resulting nef file as a byte array
        """
        return self.__nef.serialize()

    def generate_manifest_file(self) -> bytes:
        """
        Generates the .manifest metadata file

        :return: the resulting manifest as a byte array
        """
        data: Dict[str, Any] = self.__get_manifest_info()
        json_data: str = json.dumps(data, indent=4)
        return bytes(json_data, sys.getdefaultencoding())

    def __get_manifest_info(self) -> Dict[str, Any]:
        """
        Gets the manifest information in a dictionary format

        :return: a dictionary with the manifest information
        """
        # TODO: fill the information of the manifest
        return {
            "groups": [],
            "features": {
                "storage": False,
                "payable": False
            },
            "abi": self.__get_abi_info(),
            "permissions": [
                {
                    "contract": "*",
                    "methods": "*"
                }
            ],
            "trusts": [],
            "safeMethods": [],
            "extra": None
        }

    def generate_abi_file(self) -> bytes:
        """
        Generates the .abi metadata file

        :return: the resulting abi as a byte array
        """
        data: Dict[str, Any] = self.__get_abi_info()
        json_data: str = json.dumps(data)
        return bytes(json_data, sys.getdefaultencoding())

    def __get_abi_info(self) -> Dict[str, Any]:
        """
        Gets the abi information in a dictionary format

        :return: a dictionary with the abi information
        """
        return {
            "hash": self.__nef_hash,
            "methods": self.__get_abi_methods(),
            "entryPoint": self.__get_abi_entry_point(),
            "events": self.__get_abi_events()
        }

    def __get_abi_methods(self) -> List[Dict[str, Any]]:
        """
        Gets the abi methods in a dictionary format

        :return: a dictionary with the abi methods
        """
        entry_point = self.__entry_point
        if entry_point is not None:
            entry_point = entry_point[0]    # method id

        methods = []
        for method_id, method in self.__methods.items():
            if method_id != entry_point:
                logging.info("'{0}' method included in the ABI".format(method_id))
                methods.append(self.__construct_abi_method(method_id, method))
        return methods

    def __get_abi_entry_point(self) -> Dict[str, Any]:
        """
        Gets the abi entry point method in a dictionary format

        :return: a dictionary with the abi entry point
        """
        if self.__entry_point is None:
            return {}
        else:
            method_id, method = self.__entry_point
            return self.__construct_abi_method(method_id, method)

    def __construct_abi_method(self, method_id: str, method: Method) -> Dict[str, Any]:
        params = []
        for arg_id, arg in method.args.items():
            params.append({
                "name": arg_id,
                "type": arg.type.abi_type
            })
        return {
            "name": method_id,
            "parameters": params,
            "returnType": method.type.abi_type
        }

    def __get_abi_events(self) -> List[Dict[str, Any]]:
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
