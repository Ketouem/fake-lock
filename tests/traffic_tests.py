import json
from unittest import TestCase

from nose.tools import assert_list_equal, assert_true, eq_
import responses

from fake_lock.traffic import Traffic, TrafficJSONDecoder, TrafficWrapper


class TrafficDecoderTest(TestCase):

    def test_001_handle_nice_payload(self):
        payload = ('{"host1":{"left": 42, "bytes": 12, "links": 12, '
                   '"limit": "8", "type": "links", "extra": 20, '
                   '"reset": "daily"}}')
        results = json.loads(payload, cls=TrafficJSONDecoder)
        assert_true(isinstance(results, list))
        assert_true(isinstance(results[0], Traffic))
        tf = results[0]
        eq_(tf.name, 'host1')
        eq_(tf.type, 'links')

    def test_002_handle_invalid_payload(self):
        payload = '[1,2,3]'
        results = json.loads(payload, cls=TrafficJSONDecoder)
        assert_list_equal(results, [1, 2, 3])


class TrafficWrapperTest(TestCase):

    def setUp(self):
        self._wrapper = TrafficWrapper('TOKEN')

    @responses.activate
    def test_001_fetch_traffic_info(self):
        payload = ('{"host1":{"left": 42, "bytes": 12, "links": 12, '
                   '"limit": "8", "type": "links", "extra": 20, '
                   '"reset": "daily"}}')
        responses.add(
            responses.GET,
            'https://api.real-debrid.com/rest/1.0/traffic',
            status=200,
            body=payload,
            content_type='application/json'
        )
        infos = self._wrapper.get_traffic_info()
        assert_true(isinstance(infos, list))
        assert_true(isinstance(infos[0], Traffic))
        tf = infos[0]
        eq_(tf.name, 'host1')
        eq_(tf.type, 'links')
