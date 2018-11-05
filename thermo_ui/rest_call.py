import urllib.request
from urllib.error import URLError
from urllib.parse import urlencode
import json
import logging


class RestServiceCall(object):
    GET_PATH = "https://uz4ix1bqhh.execute-api.us-east-1.amazonaws.com/prod/get-zone-temperature"
    SET_PATH = "https://uz4ix1bqhh.execute-api.us-east-1.amazonaws.com/prod/set-zone-temperature"
    AWAY_PATH = "https://uz4ix1bqhh.execute-api.us-east-1.amazonaws.com/prod/set-away"

    def get_thermostat_data(self,refresh):
        data = {'refresh': refresh}
        headers = {'Content-type': 'application/json'}
        data = json.dumps(data).encode("utf-8")
        response_obj = self._http_call(RestServiceCall.GET_PATH, data, headers)
        ret_val = {'set_point': 'NA', 'temperature': 'NA', 'time': 'NA', 'battery': 'NA', 'away': False,
                   'humidity': 'NA'}
        logging.debug("get_thermostat_data response_obj = {}".format(response_obj))
        if response_obj is not None and 'state' in response_obj['body']:
            if 'reported' in response_obj['body']['state']:
                ret_val = response_obj['body']['state']['reported']
        return ret_val

    def set_thermostat_data(self, temperature):
        data = {'set_point': temperature}
        headers = {'Content-type': 'application/json'}
        data = json.dumps(data).encode("utf-8")
        response_obj = self._http_call(RestServiceCall.SET_PATH, data, headers)
        ret_val = {}
        if response_obj is not None:
            ret_val = response_obj
        logging.debug("set_thermostat_data response_obj = {}".format(response_obj))
        return ret_val

    def set_thermostat_away(self, away):
        data = {'away': away}
        headers = {'Content-type': 'application/json'}
        data = json.dumps(data).encode("utf-8")
        response_obj = self._http_call(RestServiceCall.AWAY_PATH, data, headers)
        ret_val = {}
        if response_obj is not None:
            ret_val = response_obj
        logging.debug("set_thermostat_away response_obj = {}".format(response_obj))
        return ret_val

    def _http_call(self, uri_path, data=None, headers={}, query_params=None, ret_json=True):
        url = uri_path
        if query_params is not None:
            url += "?" + urlencode(query_params)

        try:
            request_url = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(request_url, data=data) as response:
                data = response.read()
                encoding = response.info().get_content_charset('utf-8')
                ret_val = data.decode(encoding)
                if ret_json:
                    ret_val = json.loads(ret_val)
        except URLError:
            logging.debug("whoops")
            ret_val = None

        return ret_val


def main():
    print("start")
    rest_service_call = RestServiceCall()
    # rest_service_call.set_thermostat_data(83)
    rest_service_call.get_thermostat_data()


if __name__ == "__main__":
    main()
