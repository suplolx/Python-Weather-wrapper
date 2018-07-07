import requests

from DarkSkyAPI.DSForecast import DSFCurrent, DSFDaily, DSFHourly
from DarkSkyAPI.DS_logger import logger


class DarkSkyClient:

    base_url = "https://api.darksky.net/forecast/{}/{},{}?units={}"
    API_calls_remaining = 1000

    def __init__(self, api_key:str, location:tuple, units:str="si"):
        self.api_key = api_key
        self._location = location
        self._latitude = None
        self._longitude = None
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

    # TODO: implement option for setting amount of days
    def get_daily(self):
        return DSFDaily(self.raw_data['daily'])

    # TODO: implement option for setting amount of hours
    def get_hourly(self):
        return DSFHourly(self.raw_data['hourly'])

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


class BingGeoCode:

    base_url = "http://dev.virtualearth.net/REST/v1/Locations/?"

    def __init__(self, api_key, location, country:str=None):
        self.api_key = api_key
        self._country = country
        self._location = location

    def _url_builder(self):
        if self.country:
            return self.base_url + "countryRegion={}&locality={}&key={}".format(
                self.country, self.location, self.api_key)
        else:
            return self.base_url + "locality={}&key={}".format(self.location, self.api_key)

    def _get_response(self):
        raw_response = requests.get(self._url_builder())
        return raw_response.json()

    @property
    def country(self):
        return self._country

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, val):
        self._location = val

    @property
    def coords(self):
        data = self._get_response()
        logger.info(f"Setting coords for {data['resourceSets'][0]['resources'][0]['name']}")
        if data['resourceSets'][0]['estimatedTotal'] > 1 and not self.country:
            logger.warning(f"There are more than 1 locations called: {self.location}. Specify a country name as such:\n" 
                           f"GeoCode({self.api_key}, \"Amsterdam\", country=\"NL\")\n"
                           f"Location now set for {data['resourceSets'][0]['resources'][0]['name']}")
            logger.debug([name['name'] for name in data['resourceSets'][0]['resources']])
        if 'point' in data['resourceSets'][0]['resources'][0]:
            location = data['resourceSets'][0]['resources'][0]['point']['coordinates']
            coords = (location[0], location[1])
            return coords
        else:
            return None

    def __repr__(self):
        return "GeoCode({}, {})".format(self.api_key, self.location)

    def __str__(self):
        return self.coords
