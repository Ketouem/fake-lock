import json

from fake_lock import _BaseUnserializedObject, _BaseWrapper


class Traffic(_BaseUnserializedObject):

    FIELDS = {'left', 'bytes', 'links', 'limit', 'type', 'extra', 'reset'}


class TrafficJSONDecoder(json.JSONDecoder):

    def decode(self, s):
        o = json.loads(s)
        if isinstance(o, dict):
            tfs = []
            for host in o:
                tfs.append(Traffic(name=host, **o[host]))
            return tfs
        return super(self.__class__, self).decode(s)


class TrafficWrapper(_BaseWrapper):

    ENDPOINT = "/traffic"
    JSON_DECODER = TrafficJSONDecoder

    def get_traffic_info(self):
        return self._r('get')
