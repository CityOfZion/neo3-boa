import os

PROJECT_ROOT_DIRECTORY = '/'.join(os.path.dirname(__file__).split(os.sep)[:-1])

# If you didn't install TestEngine in this project's root folder, change this to the path of your .dll folder
TEST_ENGINE_DIRECTORY = ""

TEST_ENGINE_DIRECTORY_DEFAULT = '{0}/Neo.TestEngine'.format(PROJECT_ROOT_DIRECTORY)
TEST_ENGINE_DIRECTORY_ENV = os.getenv("BOA_TEST_ENGINE")

if TEST_ENGINE_DIRECTORY_ENV is not None and len(TEST_ENGINE_DIRECTORY_ENV) > 0:
    TEST_ENGINE_DIRECTORY = TEST_ENGINE_DIRECTORY_ENV
else:
    TEST_ENGINE_DIRECTORY = TEST_ENGINE_DIRECTORY_DEFAULT
