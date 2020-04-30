from boa3.compiler.generator import Generator


class Compiler:
    """
    The main compiler class.

    :ivar bytecode: the compiled file as a byte array. Empty by default.
    :ivar __generator: the object that generates the files
    """

    def __init__(self):
        self.bytecode: bytearray = bytearray()
        self.__generator: Generator = Generator()

    def compile(self, path: str) -> bytearray:
        """
        Load a Python file and tries to compile it

        :param path: the path of the Python file to compile
        :return: the bytecode of the compiled .nef file
        """
        self.__analyse(path)
        return self.__compile()

    def compile_and_save(self, path: str, output_path: str):
        """
        Save the compiled file and the metadata files

        :param path: the path of the Python file to compile
        :param output_path: the path to save the generated files
        """
        self.__analyse(path)
        self.__compile()
        self.__save(output_path)

    def __analyse(self, path: str):
        """
        Load a Python file and analysis its syntax

        :param path: the path of the Python file to compile
        """
        pass

    def __compile(self) -> bytearray:
        """
        Compile the analysed Python file.

        :return: the compiled file as a bytecode.
        :raise NotLoadedException: raised if none file were analysed
        """
        pass

    def __save(self, output_path: str):
        """
        Save the compiled file and the metadata files

        :param output_path: the path to save the generated files
        :raise NotLoadedException: raised if no file were compiled
        """
        pass
