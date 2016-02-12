import json

from fake_lock import _BaseUnserializedObject, _BaseWrapper


class Host(_BaseUnserializedObject):

    FIELDS = {'id', 'name', 'image'}


class HostStatus(_BaseUnserializedObject):

    FIELDS = {'supported', 'status', 'check_time', 'competitors_status'}


class HostsJSONDecoder(json.JSONDecoder):

    def decode(self, s):
        o = json.loads(s)
        if isinstance(o, dict):
            hts = []
            for ht in o:
                hts.append(Host(domain=ht, **Host.filter(o[ht])))
            return hts
        return super(self.__class__, self).decode(s)


class HostStatusJSONDecoder(json.JSONDecoder):

    def decode(self, s):
        o = json.loads(s)
        if isinstance(o, dict):
            sts = []
            for st in o:
                host = Host(domain=st, **Host.filter(o[st]))
                status = HostStatus(**HostStatus.filter(o[st]))
                host.status = status

                competitors = []
                for c in status.competitors_status:
                    ch = Host(domain=c)
                    cs = HostStatus(
                        **HostStatus.filter(status.competitors_status[c])
                    )
                    ch.status = cs
                    competitors.append(ch)
                host.status.competitors_status = competitors

                sts.append(host)
            return sts
        return super(self.__class__, self).decode(s)


class PassthroughJSONDecoder(json.JSONDecoder):

    def decode(self, s):
        return json.loads(s)


class HostsWrapper(_BaseWrapper):

    ENDPOINT = "/hosts"
    JSON_DECODER = HostsJSONDecoder

    def get_hosts(self):
        return self._r('get')

    def get_hosts_statuses(self):
        return self._r(
            'get',
            endpoint=(self.ENDPOINT + '/status'),
            decoder=HostStatusJSONDecoder
        )

    def get_hosts_regex(self):
        return self._r(
            'get',
            endpoint=(self.ENDPOINT + '/regex'),
            decoder=PassthroughJSONDecoder
        )

    def get_hosts_domains(self):
        return self._r(
            'get',
            endpoint=(self.ENDPOINT + '/domains'),
            decoder=PassthroughJSONDecoder
        )
