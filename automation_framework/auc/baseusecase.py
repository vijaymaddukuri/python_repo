import sys
import traceback
import unittest
import warnings
from unittest.case import SkipTest, expectedFailure, _UnexpectedSuccess

from robot.api import logger
from robot.errors import ExecutionFailed


class BaseUseCase(unittest.TestCase):
    """
        Unittest functionality will be perform below actions:
            Take the input arguments
            Validate the input arguments
            RUN the procedures
            Reset the settings to clean up
    """
    def __init__(self, name=None, method_name='run_test',
                 ctx_in=None, ctx_out=None):
        super(BaseUseCase, self).__init__(method_name)

        self._name = name or self.__class__.__name__
        self.ctx_in = ctx_in
        self.ctx_out = ctx_out

    def setUp(self):
        """
        Description: Validate the inputs passed
        """
        if self.ctx_in:
            self._validate_context()

    def tearDown(self):
        """
        Description: Finalize the involved test context
        """
        self._finalize_context()

        logger.info('[AUC] - "{}" - PASSED'.format(
            ' '.join([word.capitalize()
                      for word in self._name.split('_')])), False, True)

    def run(self, result=None):
        """
        Overwrite the behaviors of catching exceptions
        - failureExceptions will be treated as robot ExecutionFailed and
            won't fail the followed test case
        - other Exceptions will be bubbled up to higher level
        """
        rv = None
        orig_result = result
        if result is None:
            result = self.defaultTestResult()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()

        self._resultForDoCleanups = result
        result.startTest(self)

        testMethod = getattr(self, self._testMethodName)
        if (getattr(self.__class__, "__unittest_skip__", False)
            or getattr(testMethod, "__unittest_skip__", False)):
            # If the class or method was skipped.
            try:
                skip_why = (getattr(self.__class__, '__unittest_skip_why__', '')
                            or getattr(testMethod, '__unittest_skip_why__', ''))
                self._addSkip(result, skip_why)
            finally:
                result.stopTest(self)
            return
        try:
            success = False
            try:
                self.setUp()
            except SkipTest as e:
                self._addSkip(result, str(e))
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, sys.exc_info())
                raise
            else:
                try:
                    rv = testMethod()
                except KeyboardInterrupt:
                    raise
                except self.failureException as ex:
                    result.addFailure(self, sys.exc_info())

                    import traceback

                    tb = traceback.format_tb(sys.exc_info()[-1])
                    msg = 'Within "<b>{}</b>" AUC,<p> <b>Code Stack:</b>\n{}'.format(
                        self._name,
                        ''.join(tb[1:-1])
                    )
                    logger.debug(msg=msg, html=True)

                    logger.error(ex.message)
                    raise ExecutionFailed(ex.message, continue_on_failure=True)
                except expectedFailure(_UnexpectedSuccess) as e:
                    addExpectedFailure = getattr(result, 'addExpectedFailure', None)
                    if addExpectedFailure is not None:
                        addExpectedFailure(self, e.exc_info)
                    else:
                        warnings.warn("TestResult has no addExpectedFailure method, reporting as passes",
                                      RuntimeWarning)
                        result.addSuccess(self)
                except _UnexpectedSuccess:
                    addUnexpectedSuccess = getattr(result, 'addUnexpectedSuccess', None)
                    if addUnexpectedSuccess is not None:
                        addUnexpectedSuccess(self)
                    else:
                        warnings.warn("TestResult has no addUnexpectedSuccess method, reporting as failures",
                                      RuntimeWarning)
                        result.addFailure(self, sys.exc_info())
                except SkipTest as e:
                    self._addSkip(result, str(e))
                except:
                    result.addError(self, sys.exc_info())
                    raise
                else:
                    success = True

                try:
                    self.tearDown()
                except KeyboardInterrupt:
                    raise
                except:
                    result.addError(self, sys.exc_info())
                    success = False
                    raise

            cleanUpSuccess = self.doCleanups()
            success = success and cleanUpSuccess
            if success:
                result.addSuccess(self)
        finally:
            result.stopTest(self)
            if orig_result is None:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()
            return rv

    def _validate_context(self):
        pass

    def _finalize_context(self):
        pass
