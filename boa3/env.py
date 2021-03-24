import os

PROJECT_ROOT_DIRECTORY = '/'.join(os.path.dirname(__file__).split(os.sep)[:-1])

# If you didn't install TestEngine in this project's root folder, change this to the path of your .dll folder
TEST_ENGINE_DIRECTORY = '{0}/Neo.TestEngine'.format(PROJECT_ROOT_DIRECTORY)
