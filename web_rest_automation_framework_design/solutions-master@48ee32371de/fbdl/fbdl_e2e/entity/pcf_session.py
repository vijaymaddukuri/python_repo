import urlparse

from svcacroe.restacore import ISession, ICredential


class PCFSession(ISession):
    """
    Session class for holding the authorization token (Bearer ID)
    """
    # Implementation
    def __init__(self, username, password,
                 api_url, uaa_url):
        self.api_url = api_url
        self.uaa_url = uaa_url
        super(PCFSession, self).__init__(
            username=username, password=password, hostname=None)

    def _set_auth(self):
        self.credential = BearerCredential(
            self.username, self.password,
            self.api_url, self.uaa_url
        )

        _headers = {
                "Accept": 'application/json',
                "Content-Type": 'application/x-www-form-urlencoded',
                "Authorization": 'Basic Y2Y6'
            }

        _data = 'username={username}&password={password}&grant_type={grant_type}'.format(
            username=self.credential.username,
            password=self.credential.password,
            grant_type='password')

        _endpoint = 'oauth/token'

        _response = self.post(
            urlparse.urljoin(self.credential.uaa_url, _endpoint),
            headers=_headers,
            data=_data,
            verify=False
        )

        if _response.ok:
            _headers['Authorization'] = 'bearer {}'.format(_response.json()['access_token'])
        else:
            raise RuntimeError(
                'Failed to get authorization token: response code is: ' +
                _response.status_code
            )

        self.auth = self._RestBearerAuth(_headers)
        self.api_url = self.credential.api_url

    from requests.auth import AuthBase

    class _RestBearerAuth(AuthBase):
        """
        Custom authorization for PCF REST requests
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


class BearerCredential(ICredential):
    def __init__(self, username, password, api_rul, uaa_url):
        if (not api_rul) or \
                (not isinstance(api_rul, basestring)):
            raise ValueError('Non-deterministic credential: api_url')

        if (not uaa_url) or \
                (not isinstance(uaa_url, basestring)):
            raise ValueError('Non-deterministic credential: uaa_url')

        self.api_url = api_rul
        self.uaa_url = uaa_url

        super(BearerCredential, self).__init__(
            username=username, password=password)
