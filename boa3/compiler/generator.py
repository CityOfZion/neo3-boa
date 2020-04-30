class Generator:
    """
    This class is responsible for generating the files.
    """

    def generate_nef_file(self) -> bytearray:
        """
        Generates the .nef file

        :return: the resulting nef file as a byte array
        """
        pass

    def generate_manifest_file(self) -> bytearray:
        """
        Generates the .manifest metadata file

        :return: the resulting manifest as a byte array
        """
        pass

    def generate_abi_file(self) -> bytearray:
        """
        Generates the .abi metadata file

        :return: the resulting abi as a byte array
        """
        pass

    def generate_avmdbgnfo_file(self) -> bytearray:
        """
        Generates a debug map for NEO debugger

        :return: the resulting map as a byte array
        """
        pass
