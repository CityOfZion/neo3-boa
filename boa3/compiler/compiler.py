import logging
import os

from boa3.analyser.analyser import Analyser
from boa3.compiler.codegenerator.codegenerator import CodeGenerator
from boa3.compiler.filegenerator import FileGenerator
from boa3.exception.NotLoadedException import NotLoadedException


class Compiler:
    """
    The main compiler class.

    :ivar bytecode: the compiled file as a byte array. Empty by default.
    """

    def __init__(self):
        self.bytecode: bytearray = bytearray()
        self._analyser: Analyser = None
        self._entry_smart_contract: str = ''

    def compile(self, path: str, log: bool = True) -> bytes:
        """
        Load a Python file and tries to compile it

        :param path: the path of the Python file to compile
        :param log: if compiler errors should be logged.
        :return: the bytecode of the compiled .nef file
        """
        fullpath = os.path.realpath(path)
        filepath, filename = os.path.split(fullpath)

        logging.info('Started compiling\t{0}'.format(filename))
        self._entry_smart_contract = os.path.splitext(filename)[0]
        self._analyse(fullpath, log)
        return self._compile()

    def compile_and_save(self, path: str, output_path: str, log: bool = True):
        """
        Save the compiled file and the metadata files

        :param path: the path of the Python file to compile
        :param output_path: the path to save the generated files
        :param log: if compiler errors should be logged.
        """
        self.bytecode = self.compile(path, log)
        self._save(output_path)

    def _analyse(self, path: str, log: bool = True):
        """
        Load a Python file and analyses its syntax

        :param path: the path of the Python file to compile
        :param log: if compiler errors should be logged.
        """
        self._analyser = Analyser.analyse(path, log)

    def _compile(self) -> bytes:
        """
        Compile the analysed Python file.

        :return: the compiled file as a bytecode.
        :raise NotLoadedException: raised if none file were analysed
        """
        if not self._analyser.is_analysed:
            raise NotLoadedException
        return CodeGenerator.generate_code(self._analyser)

    def _save(self, output_path: str):
        """
        Save the compiled file and the metadata files

        :param output_path: the path to save the generated files
        :raise NotLoadedException: raised if no file were compiled
        """
        if (self._analyser is None
                or not self._analyser.is_analysed
                or len(self.bytecode) == 0):
            raise NotLoadedException

        generator = FileGenerator(self.bytecode, self._analyser, self._entry_smart_contract)
        with open(output_path, 'wb+') as nef_file:
            nef_bytes = generator.generate_nef_file()
            nef_file.write(nef_bytes)
            nef_file.close()

        with open(output_path.replace('.nef', '.manifest.json'), 'wb+') as manifest_file:
            manifest_bytes = generator.generate_manifest_file()
            manifest_file.write(manifest_bytes)
            manifest_file.close()

        from zipfile import ZipFile, ZIP_DEFLATED
        with ZipFile(output_path.replace('.nef', '.nefdbgnfo'), 'w', ZIP_DEFLATED) as nef_debug_info:
            debug_bytes = generator.generate_nefdbgnfo_file()
            nef_debug_info.writestr(os.path.basename(output_path.replace('.nef', '.debug.json')), debug_bytes)
