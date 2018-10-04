from auc.baseusecase import BaseUseCase


class CloseBrowser(BaseUseCase):
    """
    Close the launched browser
    """

    def test_close_browser(self):
        """
        Close the browser based on the instance from launch browser
        """
        self.ctx_in.instance.close()

    def run_test(self):
        """
        Execute the procedure to close browser
        """
        self.test_close_browser()

    def _validate_context(self):
        """
        Validate the inputs passed to this function
        """
        if self.ctx_in:
            assert self.ctx_in.instance is not None

    def _finalize_context(self):
        """
        Returns the procedure output and driver instance to re-use in other auc's
        :return: browser instance and testcase output
        """
        setattr(self.ctx_out, 'instance', None)