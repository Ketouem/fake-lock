from fake_lock import _BaseWrapper


class User(_BaseWrapper):

    ENDPOINT = "/user"

    def user(self):
        response = self._r('get')
        return response
