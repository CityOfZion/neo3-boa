import logging
import os

from boa3.analyser.analyser import Analyser
from boa3.compiler.codegenerator import CodeGenerator
from boa3.compiler.filegenerator import FileGenerator
from boa3.exception.NotLoadedException import NotLoadedException


class Compiler:
    """
    The main compiler class.

    :ivar bytecode: the compiled file as a byte array. Empty by default.
    """

    def __init__(self):
        self.bytecode: bytearray = bytearray()
        self.__analyser: Analyser = None

    def compile(self, path: str) -> bytes:
        """
        Load a Python file and tries to compile it

        :param path: the path of the Python file to compile
        :return: the bytecode of the compiled .nef file
        """
        fullpath = os.path.realpath(path)
        filepath, filename = os.path.split(fullpath)

        logging.info('Started compiling\t{0}'.format(filename))
        self.__analyse(path)
        return self.__compile()

    def compile_and_save(self, path: str, output_path: str):
        """
        Save the compiled file and the metadata files

        :param path: the path of the Python file to compile
        :param output_path: the path to save the generated files
        """
        self.bytecode = self.compile(path)
        self.__save(output_path)

    def __analyse(self, path: str):
        """
        Load a Python file and analyses its syntax

        :param path: the path of the Python file to compile
        """
        self.__analyser = Analyser.analyse(path)

    def __compile(self) -> bytes:
        """
        Compile the analysed Python file.

        :return: the compiled file as a bytecode.
        :raise NotLoadedException: raised if none file were analysed
        """
        if not self.__analyser.is_analysed:
            raise NotLoadedException
        return CodeGenerator.generate_code(self.__analyser)

    def __save(self, output_path: str):
        """
        Save the compiled file and the metadata files

        :param output_path: the path to save the generated files
        :raise NotLoadedException: raised if no file were compiled
        """
        if (self.__analyser is None
                or not self.__analyser.is_analysed
                or len(self.bytecode) == 0):
            raise NotLoadedException

        generator = FileGenerator(self.bytecode, self.__analyser.symbol_table)

        nef_bytes = generator.generate_nef_file()
        with open(output_path, 'wb+') as nef_file:
            nef_file.write(nef_bytes)
            nef_file.close()

        manifest_path = output_path.replace('.nef', '.manifest.json')
        manifest_bytes = generator.generate_manifest_file()
        with open(manifest_path, 'wb+') as manifest_file:
            manifest_file.write(manifest_bytes)
            manifest_file.close()
