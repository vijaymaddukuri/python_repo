from requests.sessions import Session

__author__ = 'GSE Automation'


class ISession(Session):
    """
    Session interface with authorization feature
    """
    def __init__(self, username, password,
                 hostname=None):
        self.username = username
        self.password = password
        self.hostname = hostname

        super(ISession, self).__init__()
        self.verify = False
        self._set_auth()

    def get(self, url, **kwargs):
        """Sends a GET request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """

        kwargs.setdefault('timeout', 60)
        kwargs.setdefault('allow_redirects', True)
        return self.request('GET', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        """Sends a POST request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """

        kwargs.setdefault('timeout', 60)
        return self.request('POST', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        """Sends a PUT request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """

        kwargs.setdefault('timeout', 60)
        return self.request('PUT', url, data=data, **kwargs)

    def _set_auth(self):
        self.credential = ICredential(self.username, self.password)

        # raise NotImplementedError(
        #     'Authorization process must be implemented.'
        # )


class ICredential(object):
    """
    Credential interface - Required and valid information for authorization
    """
    def __init__(self, username, password):
        # Parameters validation
        if (not username) or \
                (not isinstance(username, basestring)):
            raise ValueError(
                'Non-deterministic credential: username'
            )

        if (not password) or \
                (not isinstance(password, basestring)):
            raise ValueError(
                'Non-deterministic credential: password'
            )

        self.username = username
        self.password = password
