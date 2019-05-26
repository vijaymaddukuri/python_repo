from auc.baseusecase import BaseUseCase
from selenium import webdriver


class LaunchBrowser(BaseUseCase):
    """
    Launch the browser and navigate to application home page
    """

    def test_launch_browser(self):
        """
        create a new Firefox session
        Step 1: Based on the input open the browser
        Step 2: Maximum Time to wait for the browser to come up
        Step 3: Maximize the browser window
        Step 4: Navigate to the application home page
        """
        # Step 1: Based on the input open the browser
        if self.ctx_in.browserType == 'firefox':
            #If input given is Firefox, firefox browser will open
            self.driver = webdriver.Firefox()
        elif self.ctx_in.browserType == 'chrome':
            # If input given is chrome, chrome browser will open
            self.driver = webdriver.Chrome()

        # Step 2: Maximum Time to wait for the browser to come up
        self.driver.implicitly_wait(30)

        # Step 3: Maximize the browser window
        self.driver.maximize_window()

        # Step 4: Navigate to the application home page
        self.driver.get(self.ctx_in.baseUrl)

    def run_test(self):
        """
        Description: Execute the procedure to launch browser
        """
        self.test_launch_browser()

    def _validate_input_args(self, **kwargs):
        """
        Description: Validate the session id
        Args:
        :param kwargs: session id
        :return: session id object
        """
        self.tc_number = kwargs.get('tc_number')

    def _validate_context(self):
        """
        Description: Validate the inputs passed to this function
        """
        if self.ctx_in:
            assert self.ctx_in.browserType is not None
            assert self.ctx_in.baseUrl is not None

    def _finalize_context(self):
        """
        Description: Returns the procedure output and driver instance to re-use in other auc's
        :return: browser instance and testcase output
        """
        setattr(self.ctx_out, 'instance', self.driver)