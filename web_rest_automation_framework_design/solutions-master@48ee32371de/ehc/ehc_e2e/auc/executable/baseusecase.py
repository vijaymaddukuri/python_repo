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

import unittest
import sys
import warnings

from unittest.case import SkipTest, _ExpectedFailure, _UnexpectedSuccess
from robot.errors import ExecutionFailed
from robot.api import logger


class BaseUseCase(unittest.TestCase):
    def __init__(self, name=None, method_name='runTest',
                 ctx_in=None, ctx_out=None):
        super(BaseUseCase, self).__init__(method_name)

        self._name = name or self.__class__.__name__
        self.ctx_in = ctx_in
        self.ctx_out = ctx_out

    def setUp(self):
        if self.ctx_in:
            self._validate_context()

    def tearDown(self):
        # Finalize the involved test context
        self._finalize_context()

        logger.info('[AUC] - "{}" - PASSED'.format(
            ' '.join([word.capitalize()
                      for word in self._name.split('_')])), False, True)

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

                    import traceback

                    tb = traceback.format_tb(sys.exc_info()[-1])
                    msg = 'Within "<b>{}</b>" AUC,<p> <b>Code Stack:</b>\n{}'.format(
                        self._name,
                        ''.join(tb[1:-1])
                    )
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
            result.stopTest(self)
            if orig_result is None:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()

    def _validate_context(self):
        pass

    def _finalize_context(self):
        setattr(self.ctx_out, 'context', None)
