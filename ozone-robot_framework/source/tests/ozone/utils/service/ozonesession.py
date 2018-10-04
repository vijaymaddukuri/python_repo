import urlparse
from requests.sessions import Session
import requests
requests.packages.urllib3.disable_warnings()


class OzoneSession(Session):
    """
    Session interface with authorization feature
    """
    def __init__(self, email, password, hostname):

        self.credential = BearerCredential(hostname, email, password)
        self.hostname = hostname

        super(OzoneSession, self).__init__()
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

        _headers = {
                "Accept": 'application/json',
                "Content-Type": 'application/json',
                "Authorization": 'Bearer '
            }

        _body = {
            'email': self.credential.email,
            'password': self.credential.password,
        }

        _endpoint = 'auth/local'

        _response = self.post(
            urlparse.urljoin(self.credential.hostname, _endpoint),
            headers=_headers,
            json=_body,
            verify=False
        )

        if _response.ok:
            _headers['Authorization'] += _response.json()['token']
        else:
            raise RuntimeError(
                'Failed to get authorization token: {}'.format(_response.json())
            )

        self.auth = self._RestBearerAuth(_headers)
        self.hostname = self.credential.hostname

    from requests.auth import AuthBase

    class _RestBearerAuth(AuthBase):
        """
        Custom authorization for vRA REST requests
        """
        def __init__(self, headers):
            if (not headers) or \
                    (not headers['Authorization']):
                raise ReferenceError(
                    'Failed to get the authorization key'
                )

            self.headers = headers

        def __call__(self, this):
            this.headers['Accept'] = self.headers['Accept']
            this.headers['Content-Type'] = self.headers['Content-Type']
            this.headers['Authorization'] = self.headers['Authorization']

            return this


class BearerCredential(object):
    def __init__(self, hostname, email, password):
        # Parameters validation
        if (not hostname) or \
                (not isinstance(hostname, basestring)):
            raise ValueError(
                'Non-deterministic credential: hostname'
            )
        if (not hostname) or \
                (not isinstance(email, basestring)):
            raise ValueError(
                'Non-deterministic credential: email'
            )
        if (not hostname) or \
                (not isinstance(password, basestring)):
            raise ValueError(
                'Non-deterministic credential: password'
            )

        __url = urlparse.urlparse(hostname)
        self.__scheme = 'https'

        if (not __url.scheme) or \
                (__url.scheme != self.__scheme):
            hostname = urlparse.urlparse(
                self.__scheme + '://' + __url.netloc + __url.path).geturl()

        self.hostname = hostname
        self.email = email
        self.password = password
