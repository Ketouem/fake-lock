import json
from unittest import TestCase

from nose.tools import assert_list_equal, assert_true, eq_
import responses

from fake_lock.hosts import Host, HostStatus, HostsWrapper


class HostsWrapperTest(TestCase):

    def setUp(self):
        self.payload = {
            'host.com': {
                'id': 'hst',
                'name': 'host',
                'image': 'hst.jpg'
            }
        }
        self._wrapper = HostsWrapper('TOKEN')

    def _prepare_request(self, payload=None, endpoint=None):
        if endpoint is None:
            endpoint = HostsWrapper.ENDPOINT
        else:
            endpoint = HostsWrapper.ENDPOINT + endpoint
        payload = self.payload if payload is None else payload
        responses.add(
            responses.GET,
            'https://api.real-debrid.com/rest/1.0' + endpoint,
            status=200,
            body=json.dumps(payload),
            content_type='application/json'
        )

    @responses.activate
    def test_001_get_hosts(self):
        self._prepare_request()
        hosts = self._wrapper.get_hosts()
        assert_true(isinstance(hosts, list))
        assert_true(isinstance(hosts[0], Host))
        eq_(hosts[0].domain, 'host.com')
        eq_(hosts[0].id, 'hst')
        eq_(hosts[0].name, 'host')
        eq_(hosts[0].image, 'hst.jpg')

    @responses.activate
    def test_002_get_hosts_statuses(self):
        self.payload["host.com"].update({
            'supported': 0,
            'status': 'up',
            'check_time': 'TIME',
            'competitors_status': {
                'compdomain.com': {
                    'status': 'down',
                    'check_time': 'TIME1'
                }
            }
        })
        self._prepare_request(endpoint='/status')
        hosts = self._wrapper.get_hosts_statuses()
        assert_true(isinstance(hosts, list))
        assert_true(isinstance(hosts[0], Host))
        assert_true(isinstance(hosts[0].status, HostStatus))
        eq_(hosts[0].status.supported, 0)
        eq_(hosts[0].status.status, 'up')
        eq_(hosts[0].status.check_time, 'TIME')
        assert_true(isinstance(hosts[0].status.competitors_status, list))
        assert_true(isinstance(hosts[0].status.competitors_status[0], Host))
        assert_true(isinstance(
            hosts[0].status.competitors_status[0].status,
            HostStatus)
        )
        eq_(hosts[0].status.competitors_status[0].status.status, 'down')
        eq_(hosts[0].status.competitors_status[0].status.check_time, 'TIME1')

    @responses.activate
    def test_003_get_hosts_regex(self):
        payload = ['REGEX']
        self._prepare_request(endpoint='/regex', payload=payload)
        hosts_regex = self._wrapper.get_hosts_regex()
        assert_list_equal(payload, hosts_regex)

    @responses.activate
    def test_004_get_hosts_domains(self):
        payload = ['DOMAIN1', 'DOMAIN2']
        self._prepare_request(endpoint='/domains', payload=payload)
        hosts_domains = self._wrapper.get_hosts_domains()
        assert_list_equal(payload, hosts_domains)
