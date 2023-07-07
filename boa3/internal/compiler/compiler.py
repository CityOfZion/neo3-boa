import logging
import os

from boa3.internal import constants
from boa3.internal.analyser.analyser import Analyser
from boa3.internal.compiler.codegenerator.codegenerator import CodeGenerator
from boa3.internal.compiler.compileroutput import CompilerOutput
from boa3.internal.compiler.filegenerator.filegenerator import FileGenerator
from boa3.internal.exception.NotLoadedException import NotLoadedException


class Compiler:
    """
    The main compiler class.

    :ivar result: the compiled file as a byte array. Empty by default.
    """

    def __init__(self):
        self.result: CompilerOutput = CompilerOutput(bytearray())
        self._analyser: Analyser = None
        self._entry_smart_contract: str = ''

    def compile(self, path: str, root_folder: str = None, env: str = None,
                log: bool = True, log_level: str = None,
                fail_fast: bool = True) -> bytes:
        """
        Load a Python file and tries to compile it

        :param path: the path of the Python file to compile
        :param root_folder: the root path of the project
        :param log: if compiler errors should be logged.
        :param env: specific environment id to compile.
        :param fail_fast: if should stop compilation on first error found.
        :return: the bytecode of the compiled .nef file
        """
        result = self._internal_compile(path, root_folder, env, log, log_level, fail_fast).bytecode
        self._restore_log_level()
        return result

    def _internal_compile(self, path: str, root_folder: str = None, env: str = None,
                          log: bool = True, log_level: str = None,
                          fail_fast: bool = True) -> CompilerOutput:
        fullpath = os.path.realpath(path)
        filepath, filename = os.path.split(fullpath)

        logger = logging.getLogger(constants.BOA_LOGGING_NAME)
        if log_level:
            # raise error if log level is invalid
            logger.setLevel(log_level)

        logger.setLevel(logging.INFO)  # just to show initial message
        logger.info(f'neo3-boa v{constants.BOA_VERSION}\tPython {constants.SYS_VERSION}')
        logger.info(f'Started compiling\t{filename}')
        self._change_log_level(log_level)

        self._entry_smart_contract = os.path.splitext(filename)[0]

        from boa3.internal.compiler.compiledmetadata import CompiledMetadata
        from boa3.internal.model.imports.builtin import CompilerBuiltin
        CompilerBuiltin.reset()
        CompiledMetadata.reset()

        self._analyse(fullpath, root_folder, env, log, fail_fast)
        return self._compile()

    def compile_and_save(self, path: str, output_path: str, root_folder: str = None,
                         log: bool = True, log_level: str = None,
                         debug: bool = False, env: str = None, fail_fast: bool = True):
        """
        Save the compiled file and the metadata files

        :param path: the path of the Python file to compile
        :param output_path: the path to save the generated files
        :param root_folder: the root path of the project
        :param log: if compiler errors should be logged.
        :param debug: if nefdbgnfo file should be generated.
        :param env: specific environment id to compile.
        :param fail_fast: if should stop compilation on first error found.
        """
        self.result = self._internal_compile(path, root_folder, env, log, log_level, fail_fast)
        self._save(output_path, debug)
        self._restore_log_level()

    def _change_log_level(self, log_level: str = None):
        if not log_level:
            log_level = logging.ERROR

        logger = logging.getLogger(constants.BOA_LOGGING_NAME)
        self._previous_logger_level = logger.level

        logger.setLevel(log_level)

    def _restore_log_level(self):
        if hasattr(self, '_previous_logger_level'):
            logger = logging.getLogger(constants.BOA_LOGGING_NAME)
            logger.setLevel(self._previous_logger_level)
            del self._previous_logger_level

    def _analyse(self, path: str, root_folder: str = None, env: str = None,
                 log: bool = True, fail_fast: bool = True):
        """
        Load a Python file and analyses its syntax

        :param path: the path of the Python file to compile
        :param root_folder: the root path of the project
        :param log: if compiler errors should be logged.
        :param fail_fast: if should stop compilation on first error found.
        """
        self._analyser = Analyser.analyse(path, log=log, fail_fast=fail_fast,
                                          root=root_folder, env=env, compiler_entry=True)

    def _compile(self) -> CompilerOutput:
        """
        Compile the analysed Python file.

        :return: the compiled file as a bytecode.
        :raise NotLoadedException: raised if none file were analysed
        """
        if not self._analyser.is_analysed:
            raise NotLoadedException
        analyser = self._analyser.copy()
        result = CodeGenerator.generate_code(analyser)

        if len(analyser.errors) > 0:
            # should not succeed if there are unexpected internal errors during code generation
            raise NotLoadedException
        if len(result.bytecode) == 0:
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
        is_bytecode_empty = len(self.result.bytecode) == 0
        if (self._analyser is None
                or not self._analyser.is_analysed
                or is_bytecode_empty):
            raise NotLoadedException(empty_script=is_bytecode_empty)

        if not os.path.isdir(output_path):
            output_folder = os.path.abspath(os.path.dirname(output_path))
        else:
            output_folder = os.path.abspath(output_path)

        generator = FileGenerator(self.result, self._analyser, self._entry_smart_contract)

        generator.create_folder(output_folder)

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
