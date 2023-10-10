import asyncio
import unittest


class AsyncTestSuite(unittest.TestSuite):
    def run(self, result, debug=False):
        top_level = False
        if getattr(result, '_testRunEntered', False) is False:
            result._testRunEntered = top_level = True
        async_method = []
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        for index, test in enumerate(self):
            async_method.append(self.startRunCase(index, test, result))
        if async_method:
            loop.run_until_complete(asyncio.gather(*async_method))
        loop.close()
        if top_level:
            self._tearDownPreviousClass(None, result)
            self._handleModuleTearDown(result)
            result._testRunEntered = False
        return result

    async def startRunCase(self, index, test, result):
        def _isnotsuite(test):
            try:
                iter(test)
            except TypeError:
                return True
            return False

        loop = asyncio.get_event_loop()
        if result.shouldStop:
            return False

        if _isnotsuite(test):
            self._tearDownPreviousClass(test, result)
            self._handleModuleFixture(test, result)
            self._handleClassSetUp(test, result)
            result._previousTestClass = test.__class__

            if (getattr(test.__class__, '_classSetupFailed', False) or
                    getattr(result, '_moduleSetUpFailed', False)):
                return True

        await loop.run_in_executor(None, test, result)

        if self._cleanup:
            self._removeTestAtIndex(index)


class CustomTestResult(unittest.TextTestResult):
    def startTest(self, test):
        super(unittest.TextTestResult, self).startTest(test)

    def addSuccess(self, test):
        self._write_description(test)
        super(CustomTestResult, self).addSuccess(test)

    def addError(self, test, err):
        self._write_description(test)
        super(CustomTestResult, self).addError(test, err)

    def addFailure(self, test, err):
        self._write_description(test)
        super(CustomTestResult, self).addFailure(test, err)

    def addSkip(self, test, reason):
        self._write_description(test)
        super(CustomTestResult, self).addSkip(test, reason)

    def addExpectedFailure(self, test, err):
        self._write_description(test)
        super(CustomTestResult, self).addExpectedFailure(test, err)

    def addUnexpectedSuccess(self, test):
        self._write_description(test)
        super(CustomTestResult, self).addUnexpectedSuccess(test)

    def _write_description(self, test):
        if self.showAll:
            self.stream.write(self.getDescription(test))
            self.stream.write(" ... ")
            self.stream.flush()


def list_of_tests_gen(test_suite):
    for test in test_suite:
        if hasattr(unittest.suite, '_isnotsuite') and unittest.suite._isnotsuite(test):
            yield test
        else:
            for t in list_of_tests_gen(test):
                yield t
