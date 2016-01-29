from requests import request


class _BaseWrapper:

    URL = "https://api.real-debrid.com/rest/1.0"
    ENDPOINT = None

    def __init__(self, api_token, endpoint=None):
        self._api_token = api_token
        self._endpoint = self.ENDPOINT if endpoint is None else endpoint

    def _build_headers(self, verb='get'):
        hds = {
            "Authorization": "Bearer {}".format(self._api_token),
            "Accept": "application/json"
        }
        if verb.lower() in {'post', 'put'}:
            hds.update({"Content-Type": "application/json"})
        return hds

    def _r(self, verb, data=None, endpoint=None):
        f_url = '{}{}'.format(
            self.URL,
            self._endpoint if endpoint is None else endpoint
        )
        resp = request(
            verb, f_url,
            headers=self._build_headers(verb)
        )
        if resp.status_code >= 400:
            self._handle_error_code(resp.status_code)
        if resp.headers.get('Content-Type') == 'application/json':
            return resp.json()
        else:
            return resp

    def _handle_error_code(self, code):
        if code == 401:
            raise BadTokenError()
        elif code == 403:
            raise PermissionDeniedError()

    def _disable_token(self):
        try:
            resp = self._r('get', endpoint='/disable_access_token')
            if resp.status_code == 204:
                self._api_token = None
                disabled = True
            else:
                disabled = False
        except BadTokenError:
            disabled = False
        return disabled

    def __repr__(self):
        return "<{}('{}')>".format(self.__class__.__name__, self._endpoint)


class RealException(Exception):
    pass


class BadTokenError(RealException):
    pass


class PermissionDeniedError(RealException):
    pass
