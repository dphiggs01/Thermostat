import urllib.request
from urllib.error import URLError
from urllib.parse import urlencode
import logging
import datetime
import json

logger = logging.getLogger()

class Weather:
    API_KEY = '466289658e4c868cf751a5fe8601224a'
    URI_PATH = 'http://api.openweathermap.org/data/2.5/weather'

    def __init__(self):
        self._weather_response = None

    def get_current_temperature(self):
        temp = None
        if self._weather_response is not None:
            if 'main' in self._weather_response:
                main = self._weather_response['main']
                temp = main['temp']
        return temp

    def get_current_weather_by_zip(self,zip):
        query_params = {'zip': zip, 'units': 'imperial'}
        query_params['APPID'] = Weather.API_KEY

        response_obj = self._http_call(Weather.URI_PATH, query_params)
        if response_obj is not None:
            self._weather_response = response_obj
        return self._weather_response


    def _http_call(self, uri_path, query_params=None, ret_json=True):
        url = uri_path
        if query_params is not None:
            url += "?" + urlencode(query_params)

        try:
            request_url = urllib.request.Request(url)
            with urllib.request.urlopen(request_url) as response:
                data = response.read()
                encoding = response.info().get_content_charset('utf-8')
                ret_val = data.decode(encoding)
                if ret_json:
                    ret_val = json.loads(ret_val)
        except URLError as e:
            ret_val = None
            if hasattr(e, 'reason'):
                logger.critical('We failed to reach a server.')
                logger.critical('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                logger.critical('The server couldn\'t fulfill the request.')
                logger.critical('Error code: ', e.code)
        return ret_val

if __name__ == "__main__":
    weather = Weather()
    json = weather.get_current_weather_by_zip('01543')
    print(json)
    print(weather.get_current_temperature())