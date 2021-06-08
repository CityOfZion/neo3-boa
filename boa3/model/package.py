from typing import Dict, List

from boa3.model.identifiedsymbol import IdentifiedSymbol


class Package(IdentifiedSymbol):
    """
    A class used to represent a Python module.

    :ivar properties: a list that stores every property in the package. Empty by default.
    :ivar methods: a list that stores every method in the package. Empty by default.
    :ivar types: a list that stores every property in the package. Empty by default.
    """

    def __init__(self, identifier: str,
                 properties: List[IdentifiedSymbol] = None,
                 methods: List[IdentifiedSymbol] = None,
                 types: List[IdentifiedSymbol] = None,
                 ):
        super().__init__(identifier)

        if methods is None:
            methods = []
        self.methods = methods

        if properties is None:
            properties = []
        self.properties = properties

        if types is None:
            types = []
        self.types = types

    @property
    def shadowing_name(self) -> str:
        return 'package'

    @property
    def symbols(self) -> Dict[str, IdentifiedSymbol]:
        """
        Gets all the symbols in the package.

        :return: a list that stores every symbol in the package
        """
        symbols = {}
        symbols.update({symbol.raw_identifier: symbol for symbol in self.types})
        symbols.update({symbol.raw_identifier: symbol for symbol in self.properties})
        symbols.update({symbol.raw_identifier: symbol for symbol in self.methods})
        return symbols
