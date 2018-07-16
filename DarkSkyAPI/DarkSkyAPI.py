import requests

from DarkSkyAPI.DSForecast import DSFCurrent, DSFDaily, DSFHourly
from DarkSkyAPI.DS_logger import logger

# TODO:: Add docstrings

class DarkSkyClient:

    base_url = "https://api.darksky.net/forecast/{}/{},{}?units={}"
    API_calls_remaining = 1000

    def __init__(self, api_key:str, location:tuple, units:str="si", exclude:list=None):
        self.api_key = api_key
        self._location = location
        self._latitude = None
        self._longitude = None
        self.units = units
        self.exclude = exclude
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

    def get_daily(self, days:int=7):
        return DSFDaily(self.raw_data['daily'], days)

    def get_hourly(self, hours:int=47):
        return DSFHourly(self.raw_data['hourly'], hours)

    @property
    def daily(self):
        if "daily" not in self.exclude:
            return self.get_daily()
        else:
            return None

    @property
    def hourly(self):
        if "hourly" not in self.exclude:
            return self.get_hourly()
        else:
            return None

    @property
    def current(self):
        return self.get_current()
    
    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value:tuple):
        self._location = value

    @property
    def latitude(self):
        return self._location[0]

    @latitude.setter
    def latitude(self, value:float):
        self._latitude = value

    @property
    def longitude(self):
        return self._location[1]

    @longitude.setter
    def longitude(self, value:float):
        self._longitude = value

    def __repr__(self):
        return "DarkSkyClient('{}', '{}', '{}', '{}')".format(self.api_key, self.latitude, self.longitude, self.units)

    def __str__(self):
        return "Latitude: {} - Longitude: {} - Units: {} - Timezone: {}\nRemaining calls: {}".format(
                                                                                         self.latitude, self.longitude,
                                                                                         self.units, self.timezone,
                                                                                         self.API_calls_remaining)
