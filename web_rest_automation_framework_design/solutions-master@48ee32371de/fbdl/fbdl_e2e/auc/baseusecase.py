#  Copyright 2016 EMC GSE SW Automation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import sys
import traceback
import unittest
import warnings
from unittest.case import SkipTest, _ExpectedFailure, _UnexpectedSuccess

from robot.api import logger
from robot.errors import ExecutionFailed


class BaseUseCase(unittest.TestCase):
    def __init__(self, name=None, methodName='runTest'):
        super(BaseUseCase, self).__init__(methodName)

        if name:
            self._name = name
        else:
            self._name = type(self).__name__

    def setUp(self):
        # Configure preconditions by involving test context
        pass

    def tearDown(self):
        # Finalize the involved test context
        pass

    def run(self, result=None):
        """
        Overwrite the behaviors of catching exceptions
        - failureExceptions will be treated as robot ExecutionFailed and
            won't fail the followed test case
        - other Exceptions will be bubbled up to higher level (e.g., robot framework)
        """

        orig_result = result
        if result is None:
            result = self.defaultTestResult()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()

        self._resultForDoCleanups = result
        result.startTest(self)

        testMethod = getattr(self, self._testMethodName)
        if (getattr(self.__class__, "__unittest_skip__", False) or
            getattr(testMethod, "__unittest_skip__", False)):
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

            # logger.info('Testing on "{}" test case - GET STARTED'
            #             .format(type(self).__name__), False, True)

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
                    testMethod()
                except KeyboardInterrupt:
                    raise
                except self.failureException as ex:
                    result.addFailure(self, sys.exc_info())
                    tb = traceback.format_tb(sys.exc_info()[-1])
                    msg = 'Within "<b>{}</b>" AUC,<p> <b>Code Stack:</b>\n{}'.format(
                        self._name, ''.join(tb[1:-1]))

                    if not self._ignore_failure():
                        logger.debug(msg=msg, html=True)
                        logger.error(ex.message)

                        raise ExecutionFailed(ex.message, continue_on_failure=True)
                except _ExpectedFailure as e:
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
            if result.failures or result.errors:
                status = 'FAILED'
            else:
                status = 'PASSED'

            logger.info('[AUC] - "{}" - {}'.format(
                ' '.join([word.capitalize()
                          for word in self._name.split('_')]),
                status), False, True)

            result.stopTest(self)
            if orig_result is None:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()

    def _ignore_failure(self, debug_only=True):
        if debug_only:
            import inspect
            for frame in inspect.stack()[::-1]:
                if frame[1].endswith('pydevd.py'):
                    return True
            else:
                return False

        return False
