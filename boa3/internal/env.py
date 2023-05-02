import os

from boa3.internal import constants

PROJECT_ROOT_DIRECTORY = constants.PATH_SEPARATOR.join(os.path.dirname(__file__).split(os.sep)[:-2])

# If you don't want to use the neo-express instance on boa3_test/tests on a lot of test, then change this path to
# another one, otherwise you could just pass the neoxp_path parameter when instantiating NeoTestRunner
NEO_EXPRESS_INSTANCE_DIRECTORY = f'{PROJECT_ROOT_DIRECTORY}/boa3_test/tests'
TEST_RUNNER_DIRECTORY = os.path.abspath('.')
