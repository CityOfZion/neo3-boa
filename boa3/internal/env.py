import os

from boa3.internal import constants

PROJECT_ROOT_DIRECTORY = constants.PATH_SEPARATOR.join(os.path.dirname(__file__).split(os.sep)[:-2])

TEST_RUNNER_DIRECTORY = os.path.abspath('.')
