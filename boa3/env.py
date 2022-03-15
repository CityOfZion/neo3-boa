import os

from boa3 import constants

PROJECT_ROOT_DIRECTORY = constants.PATH_SEPARATOR.join(os.path.dirname(__file__).split(os.sep)[:-1])

# If you didn't install TestEngine in this project's root folder, change this to the path of your .dll folder
TEST_ENGINE_DIRECTORY = f'{PROJECT_ROOT_DIRECTORY}{constants.PATH_SEPARATOR}Neo.TestEngine'
