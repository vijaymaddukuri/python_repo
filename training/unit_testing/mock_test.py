import unittest

from unit_testing.mock_example import MyService

from training.unit_testing.single_sign_on import *

class MyServiceTest(unittest.TestCase):
    def test_invalid_token(self):
        registry = FakeSingleSignOnRegistry()
        my_service = MyService(registry)

        response = my_service.handle_request("do stuff", token=None)
        self.assertIn("Please enter the login details", response)

    def test_valid_token(self):
        registry = FakeSingleSignOnRegistry()
        token = registry.register("valid credentials")
        my_service = MyService(registry)

        response = my_service.handle_request("do stuff", token)
        self.assertIn("Hello World", response)

    def test_valid_token_with_mock(self):
        token = SSOToken()
        registry = MockSingleSignOnRegistry(expected_token=token, token_is_valid=True)
        my_service = MyService(registry)

        response = my_service.handle_request("do stuff", token)
        self.assertTrue(registry.is_valid_was_called)

    def test_invalid_token_with_mock(self):
        token = SSOToken()
        registry = MockSingleSignOnRegistry(expected_token=token, token_is_valid=False)
        my_service = MyService(registry)

        response = my_service.handle_request("do stuff", token)
        self.assertTrue(registry.is_valid_was_called)

    def test_invalid_token_with_spy(self):
        token = SSOToken()
        registry = SpySingleSignOnRegistry(accept_all_tokens=False)
        my_service = MyService(registry)

        response = my_service.handle_request("do stuff", token)
        self.assertTrue(registry.checked_tokens)

    def test_valid_token_with_spy(self):
        token = SSOToken()
        registry = SpySingleSignOnRegistry(accept_all_tokens=True)
        my_service = MyService(registry)

        response = my_service.handle_request("do stuff", token)
        self.assertTrue(registry.checked_tokens)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
