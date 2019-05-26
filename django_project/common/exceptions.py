class TenantCreationException(Exception):
    pass


class TASException(Exception):
    """
    This class is exception handler for TAS.
    :param err_code: Error code defined by the caller.
    :param err_message: Error message is User friendly message,
                           this message is defined by app.
    :param err_trace: Actual output.
    """
    def __init__(self, err_code=None, err_message=None, err_trace=None):
        self.err_code = err_code
        self.err_message = err_message
        self.err_trace = err_trace


class APIException(Exception):
    def __init__(self, custom_message, received_message):
        self.custom_message = custom_message
        self.received_message = received_message


class SALTException(Exception):
    def __init__(self, error_message, salt_resp):
        self.error_message = error_message
        self.salt_resp = salt_resp
