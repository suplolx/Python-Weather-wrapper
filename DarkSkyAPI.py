import requests
from DSForecast import DSFCurrent, DSFDaily, DSFHourly


class DarkSkyClient:

    base_url = "https://api.darksky.net/forecast/{}/{},{}?units={}"

    def __init__(self, api_key:str, lat:float, lon:float, units:str="si"):
        self.api_key = api_key
        self.latitude = lat
        self.longitude = lon
        self.units = units
        self.raw_data = self._get_response()
        self.timezone = self.raw_data['timezone']

    def _url_builder(self):
        url = self.base_url.format(self.api_key, self.latitude, self.longitude, self.units)
        return url

    def _get_response(self):
        r = requests.get(self._url_builder())
        raw_response = r.json()
        return raw_response

    def get_current(self):
        return DSFCurrent(self.raw_data['currently'])

    def get_daily(self):
        return DSFDaily(self.raw_data['daily'])

    def get_hourly(self):
        return DSFHourly(self.raw_data['hourly'])
