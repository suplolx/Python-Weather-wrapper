import requests

from DarkSkyAPI.DSForecast import DSFCurrent, DSFDaily, DSFHourly
from DarkSkyAPI.DS_logger import logger


class DarkSkyClient:

    base_url = "https://api.darksky.net/forecast/{}/{},{}?units={}"
    API_calls_remaining = 1000

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
        raw_response = requests.get(self._url_builder())
        self.API_calls_remaining -= int(raw_response.headers['X-Forecast-API-Calls'])
        logger.info(f"API calls remaining: {self.API_calls_remaining}")
        return raw_response.json()

    def get_current(self):
        return DSFCurrent(self.raw_data['currently'])

    def get_daily(self):
        return DSFDaily(self.raw_data['daily'])

    def get_hourly(self):
        return DSFHourly(self.raw_data['hourly'])

    def __repr__(self):
        return "DarkSkyClient('{}', '{}', '{}', '{}')".format(self.api_key, self.latitude, self.longitude, self.units)

    def __str__(self):
        return "Latitude: {} - Longitude: {} - Units: {} - Timezone: {}\nRemaining calls: {}".format(
                                                                                         self.latitude, self.longitude,
                                                                                         self.units, self.timezone,
                                                                                         self.API_calls_remaining)
