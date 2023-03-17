from boa3.internal.compiler.compiler import Compiler
from boa3.internal.exception.InvalidPathException import InvalidPathException


class Boa3:
    """
    The main class.
    Contains the methods that the final user have access to.
    """

    @staticmethod
    def compile(path: str, root_folder: str = None) -> bytes:
        """
        Load a Python file to be compiled but don't write the result into a file

        :param path: the path of the Python file to compile
        :param root_folder: the root path of the project
        :return: the bytecode of the compiled .nef file
        """
        if not path.endswith('.py'):
            raise InvalidPathException(path)

        return Compiler().compile(path, root_folder)

    @staticmethod
    def compile_and_save(path: str, output_path: str = None, root_folder: str = None, show_errors: bool = True, debug: bool = False):
        """
        Load a Python file to be compiled and save the result into the files.
        By default, the resultant .nef file is saved in the same folder of the
        source file.

        :param path: the path of the Python file to compile
        :param output_path: Optional path to save the generated files
        :param root_folder: the root path of the project
        :param show_errors: if compiler errors should be logged.
        :param debug: if nefdbgnfo file should be generated.
        """
        if not path.endswith('.py'):
            raise InvalidPathException(path)

        if output_path is None:
            output_path = path.replace('.py', '.nef')
        elif not output_path.endswith('.nef'):
            raise InvalidPathException(path)

        Compiler().compile_and_save(path, output_path, root_folder, show_errors, debug)
