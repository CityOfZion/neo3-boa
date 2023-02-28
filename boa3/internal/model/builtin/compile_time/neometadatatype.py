from boa3.internal.model.identifiedsymbol import IdentifiedSymbol


class __NeoMetadataType(IdentifiedSymbol):
    """
    A class used to represent the metadata object
    """

    def __init__(self):
        identifier = 'NeoMetadata'
        super().__init__(identifier)

    @property
    def shadowing_name(self) -> str:
        return 'type'

    def __str__(self) -> str:
        return self.identifier


MetadataTypeSingleton = __NeoMetadataType()
