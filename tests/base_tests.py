from unittest import TestCase

from nose.tools import (
    assert_dict_equal, assert_false, assert_is_none, assert_raises,
    assert_true, eq_
)
import responses

from fake_lock import (
    _BaseWrapper, BadTokenError, PermissionDeniedError, RealException
)


class BaseTests(TestCase):

    def setUp(self):
        self._token = 'FAKETOKEN'
        self._base = _BaseWrapper(self._token)

    def test_001_build_headers(self):
        headers = self._base._build_headers('post')
        assert_dict_equal(
            headers,
            {
                'Authorization': 'Bearer {}'.format(self._token),
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        )
        headers = self._base._build_headers('get')
        assert_dict_equal(
            headers,
            {
                'Authorization': 'Bearer {}'.format(self._token),
                'Accept': 'application/json'
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
        assert_raises(
            RealException,
            self._base._handle_error_code, 478
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

    @responses.activate
    def test_004a_test_request_response_with_json(self):
        api_response_data = {'data': 'unitTest'}
        responses.add(
            responses.GET,
            'https://api.real-debrid.com/rest/1.0/fakeEndpoint',
            status=200,
            json=api_response_data,
            content_type='application/json'
        )
        response = self._base._r('get', endpoint='/fakeEndpoint')
        assert_dict_equal(response, api_response_data)

    @responses.activate
    def test_004b_test_request_not_json(self):
        api_response_data = "<html>unittest</html>"
        responses.add(
            responses.GET,
            'https://api.real-debrid.com/rest/1.0/fakeEndpoint',
            status=200,
            body=api_response_data,
            content_type='text/html'
        )
        response = self._base._r('get', endpoint='/fakeEndpoint')
        eq_(response.status_code, 200)
        eq_(response.content, api_response_data)

    @responses.activate
    def test_004c_test_request_error(self):
        responses.add(
            responses.GET,
            'https://api.real-debrid.com/rest/1.0/fakeEndpoint',
            status=478
        )
        assert_raises(
            RealException,
            self._base._r, 'get', endpoint='/fakeEndpoint'
        )
