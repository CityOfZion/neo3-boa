import logging
import os

from boa3 import constants
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

    def compile(self, path: str, root_folder: str = None, log: bool = True) -> bytes:
        """
        Load a Python file and tries to compile it

        :param path: the path of the Python file to compile
        :param root_folder: the root path of the project
        :param log: if compiler errors should be logged.
        :return: the bytecode of the compiled .nef file
        """
        fullpath = os.path.realpath(path)
        filepath, filename = os.path.split(fullpath)

        logging.info(f'neo3-boa v{constants.BOA_VERSION}\tPython {constants.SYS_VERSION}')
        logging.info(f'Started compiling\t{filename}')
        self._entry_smart_contract = os.path.splitext(filename)[0]

        from boa3.model.imports.builtin import CompilerBuiltin
        CompilerBuiltin.reset()

        self._analyse(fullpath, root_folder, log)
        return self._compile()

    def compile_and_save(self, path: str, output_path: str, root_folder: str = None, log: bool = True, debug: bool = False):
        """
        Save the compiled file and the metadata files

        :param path: the path of the Python file to compile
        :param output_path: the path to save the generated files
        :param root_folder: the root path of the project
        :param log: if compiler errors should be logged.
        :param debug: if nefdbgnfo file should be generated.
        """
        self.bytecode = self.compile(path, root_folder, log)
        self._save(output_path, debug)

    def _analyse(self, path: str, root_folder: str = None, log: bool = True):
        """
        Load a Python file and analyses its syntax

        :param path: the path of the Python file to compile
        :param root_folder: the root path of the project
        :param log: if compiler errors should be logged.
        """
        self._analyser = Analyser.analyse(path, log=log, root=root_folder)

    def _compile(self) -> bytes:
        """
        Compile the analysed Python file.

        :return: the compiled file as a bytecode.
        :raise NotLoadedException: raised if none file were analysed
        """
        if not self._analyser.is_analysed:
            raise NotLoadedException
        analyser = self._analyser.copy()
        result = CodeGenerator.generate_code(analyser)
        if len(result) == 0:
            raise NotLoadedException(empty_script=True)

        if constants.INITIALIZE_METHOD_ID in analyser.symbol_table:
            self._analyser.symbol_table[constants.INITIALIZE_METHOD_ID] = analyser.symbol_table[constants.INITIALIZE_METHOD_ID]
        if constants.DEPLOY_METHOD_ID in analyser.symbol_table:
            self._analyser.symbol_table[constants.DEPLOY_METHOD_ID] = analyser.symbol_table[constants.DEPLOY_METHOD_ID]

        return result

    def _save(self, output_path: str, debug: bool):
        """
        Save the compiled file and the metadata files

        :param output_path: the path to save the generated files
        :raise NotLoadedException: raised if no file were compiled
        :param debug: if nefdbgnfo file should be generated.
        """
        is_bytecode_empty = len(self.bytecode) == 0
        if (self._analyser is None
                or not self._analyser.is_analysed
                or is_bytecode_empty):
            raise NotLoadedException(empty_script=is_bytecode_empty)

        generator = FileGenerator(self.bytecode, self._analyser, self._entry_smart_contract)
        with open(output_path, 'wb+') as nef_file:
            nef_bytes = generator.generate_nef_file()
            nef_file.write(nef_bytes)
            nef_file.close()

        with open(output_path.replace('.nef', '.manifest.json'), 'wb+') as manifest_file:
            manifest_bytes = generator.generate_manifest_file()
            manifest_file.write(manifest_bytes)
            manifest_file.close()

        if debug:
            from zipfile import ZipFile, ZIP_DEFLATED
            with ZipFile(output_path.replace('.nef', '.nefdbgnfo'), 'w', ZIP_DEFLATED) as nef_debug_info:
                debug_bytes = generator.generate_nefdbgnfo_file()
                nef_debug_info.writestr(os.path.basename(output_path.replace('.nef', '.debug.json')), debug_bytes)
