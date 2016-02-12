from requests import request


class _BaseWrapper:

    URL = "https://api.real-debrid.com/rest/1.0"
    ENDPOINT = None
    JSON_DECODER = None

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

    def _r(self, verb, data=None, endpoint=None, decoder=None):
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
            decoder = self.JSON_DECODER if decoder is None else decoder
            return resp.json(cls=decoder)
        else:
            return resp

    def _handle_error_code(self, code):
        if code == 401:
            raise BadTokenError()
        elif code == 403:
            raise PermissionDeniedError()
        else:
            raise RealException("Error {}".format(code))

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


class _BaseUnserializedObject:

    FIELDS = set()

    def __init__(self, **kwargs):
        for f in self.FIELDS:
            setattr(self, f, kwargs.get(f))
        for o in set(kwargs.keys()).difference(self.FIELDS):
            setattr(self, o, kwargs.get(o))

    def __repr__(self):
        return "<{}({})>".format(
            self.__class__.__name__,
            ",".join(
                "{}={}".format(k, self.__dict__[k]) for k in self.__dict__
            )
        )

    @classmethod
    def filter(cls, dico):
        return {k: dico[k] for k in cls.FIELDS if k in dico}


class RealException(Exception):
    pass


class BadTokenError(RealException):
    pass


class PermissionDeniedError(RealException):
    pass
