if __name__ == '__main__':
    import sys
    import os.path
    import shutil

    # The unit test should not be included in the neo3-boa package, so to not have an import problem, we are directly
    # adding the project root to the sys path, because the boa3_test unit test files are not in the package.
    project_root = os.path.abspath(f'{os.path.dirname(__file__)}/../..')
    sys.path.append(project_root)

    from boa3.internal import env
    from boa3_test.tests import boatestcase
    from boa3_test.tests.test_suite import *
    from boa3_test.test_drive import utils

    neo_express_dir = env.NEO_EXPRESS_INSTANCE_DIRECTORY
    env_test_runner_dir = env.TEST_RUNNER_DIRECTORY

    # avoids to have multiple applications accessing the same config file
    test_runner_dir = os.path.abspath('./test-runner')
    neo_express_exec_dir = f'{test_runner_dir}/{utils.create_custom_id("neoxp", use_time=False)}'

    try:
        if not os.path.exists(test_runner_dir):
            os.mkdir(test_runner_dir)

        if not os.path.exists(neo_express_exec_dir):
            os.mkdir(neo_express_exec_dir)

        neo_express_exec_file = f'{neo_express_exec_dir}/default.neo-express'
        shutil.copy(f'{neo_express_dir}/default.neo-express', neo_express_exec_file)
        env.NEO_EXPRESS_INSTANCE_DIRECTORY = neo_express_exec_dir
        env.TEST_RUNNER_DIRECTORY = test_runner_dir
        boatestcase.USE_UNIQUE_NAME = True

        suite = AsyncTestSuite()
        default_suite = unittest.TestSuite()
        discover_path = f'{env.PROJECT_ROOT_DIRECTORY}/boa3_test/'
        test_discover = unittest.loader.defaultTestLoader.discover(discover_path,
                                                                   top_level_dir=env.PROJECT_ROOT_DIRECTORY,
                                                                   )

        for test in list_of_tests_gen(test_discover):
            if isinstance(test, boatestcase.SmartContractTestCase):
                default_suite.addTest(test)
            else:
                suite.addTest(test)

        default_suite.addTest(suite)
        print(f'Found {default_suite.countTestCases()} tests\n')

        test_result = unittest.TextTestRunner(verbosity=2,
                                              resultclass=CustomTestResult,
                                              ).run(default_suite)

        sys.exit(not test_result.wasSuccessful())
    finally:
        # set environment variables back to their starting state
        env.NEO_EXPRESS_INSTANCE_DIRECTORY = neo_express_dir
        env.TEST_RUNNER_DIRECTORY = env_test_runner_dir
        boatestcase.USE_UNIQUE_NAME = False
        # clear test directories
        shutil.rmtree(neo_express_exec_dir)
        if len(os.listdir(test_runner_dir)) == 0:
            os.rmdir(test_runner_dir)

    sys.exit(0)
