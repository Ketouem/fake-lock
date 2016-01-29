from unittest import TestCase

from nose.tools import (
    assert_dict_equal, assert_false, assert_is_none, assert_raises,
    assert_true, eq_
)
import responses

from fake_lock import _BaseWrapper, BadTokenError, PermissionDeniedError


class BaseTests(TestCase):

    def setUp(self):
        self._token = 'FAKETOKEN'
        self._base = _BaseWrapper(self._token)

    def test_001_build_headers(self):
        headers = self._base._build_headers('post')
        assert_dict_equal(
            headers,
            {
                "Authorization": "Bearer {}".format(self._token),
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        )
        headers = self._base._build_headers('get')
        assert_dict_equal(
            headers,
            {
                "Authorization": "Bearer {}".format(self._token),
                "Accept": "application/json"
            }
        )

    def test_002_handle_error_code(self):
        assert_raises(
            BadTokenError,
            self._base._handle_error_code, 401
        )
        assert_raises(
            PermissionDeniedError,
            self._base._handle_error_code, 403
        )

    @responses.activate
    def test_003a_disable_token(self):
        responses.add(
            responses.GET,
            'https://api.real-debrid.com/rest/1.0/disable_access_token',
            status=204
        )
        assert_true(self._base._disable_token())
        assert_is_none(self._base._api_token)

    @responses.activate
    def test_003b_disable_token_bad_api_response(self):
        responses.add(
            responses.GET,
            'https://api.real-debrid.com/rest/1.0/disable_access_token',
            status=401
        )
        assert_false(self._base._disable_token())
        eq_(self._base._api_token, self._token)
