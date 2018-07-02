from datetime import datetime

from DS_logger import logger


class DSFMBase:

    def __init__(self, data:dict):
        """Constructor method.

        Sets base attributes from data dict.

        Arguments:
            data {dict} -- A dict containing the daily or hourly data from the DarkSkyAPI.

        Attributes:
            data {list} -- A list containing the day and hour forecast data
            summary {str} -- A summary of the daily or hourly forecast
            icon {str} -- A string representation of the weather icon (example: cloudy)

        """
        self.data = data['data']
        self.general_summary = data['summary']
        self.general_icon = data['icon']
        logger.info(f"{repr(self)} created")
    
    def data_pair(self, datapoint:str, t:int=None, date_fmt:str='%d-%m-%Y %H:%M', graph:bool=False):
        """Generates a list of value pairs containing datetimes and datapoint values.

        Arguments:
            datapoint {str} -- The forecast datapoint you want the values from (example: windSpeed)
            t {int} -- The amount of days/hours the user wants to return
        
        Keyword Arguments:
            date_fmt {str} -- The datetime format (default: {'%d-%m-%Y %H:%M'})
            graph {bool} --  a graph-friendly dict (default: {False})
        
        Returns:
            list -- list of tuple value pairs
            dict -- graph-friendly dict when graph set to True 
        """
        time_range = get_time_range(self, t)
        if graph:
            return dict(x=[timestamp(self.data[tr].get('time', None), date_fmt) for tr in time_range],
                        y=[self.data[tr].get(datapoint, None) for tr in time_range])
        else:
            return [(timestamp(self.data[tr].get('time', None), date_fmt), self.data[tr].get(datapoint, None)) for tr in time_range]
    
    def data_single(self, datapoint:str, t:int=None, to_percent=False, to_datetime=False):
        """Generates a list of single datapoint values.
        
        Arguments:
            datapoint {str} -- The forecast datapoint you want the values of (example: windSpeed)
            t {int} -- The amount of days/hours the user wants to return
        
        Keyword Arguments:
            to_percent {bool} -- Boolean which will convert datapoint values to precentages
            to_datetime {bool} -- Boolean which will convert datapoint values to datetime strings
        
        Returns:
            list -- A list containing single datapoint values
        """
        time_range = get_time_range(self, t)
        if to_percent:
            return [int(self.data[tr].get(datapoint, None) * 100) if datapoint in self.data[tr] else None for tr in time_range]
        elif to_datetime:
            return [timestamp(self.data[tr].get(datapoint, None), "%d-%m-%Y %H:%M") if datapoint in self.data[tr] else None for tr in time_range]
        else:
            return [self.data[tr].get(datapoint, None) if datapoint in self.data[tr] else None for tr in time_range]

    def data_combined(self, t:int=None, datalist:list=None, date_fmt="%d-%m-%Y %H:%M"):
        """Generates a custom dict of datapoint values for each day/hour.

        Arguments:
            t {int} -- The amount of days/hours the user wants to return

        Keyword Arguments:
            datalist {list} -- A list of datapoints you want the values of (default: {None})
            date_fmt {str} -- Datetime format (default: {%d-%m-%Y %H:%M})
        
        Returns:
            dict -- A dict of datapoints and their corresponding values. If no list is provided, all datapoints will
            be used.
        """
        time_range = get_time_range(self, t)
        if datalist:
            return {datapoint: [timestamp(self.data[tr].get(datapoint, None), date_fmt) if datapoint.lower().find("time") >= 0 
                    else self.data[tr].get(datapoint, None) for tr in time_range] for datapoint in datalist}
        else:
            datalist = [datakey for datakey in self.data[0].keys()]
            return {datapoint: [self.data[tr].get(datapoint, None) for tr in time_range] for datapoint in datalist}

    def datetimes(self, t:int=None, date_fmt:str="%d-%m-%Y %H:%M"):
        """Generates a list of datetime strings of all the hours/days.
        
        Arguments:
            t {int} -- The amount of days/hours the user wants to return

        Keyword Arguments:
            date_fmt {str} -- The datetime format (default: {"%d-%m-%Y %H:%M"})
        
        Returns:
            list -- A list of datetime strings of all the hours/days
        """
        time_range = get_time_range(self, t)
        return [timestamp(self.data[tr].get('time', None), date_fmt) for tr in time_range]

    def is_raining(self, n):
        return self.data[n]["precipProbability"] > 0

    @property
    def time(self):
        """list: a list of datetime strings."""
        return self.data_single('time', to_datetime=True)
    
    @property
    def summary(self):
        """list: a list of weather summary's."""
        return self.data_single('summary')

    @property
    def icon(self):
        """list: a list of weather icons."""
        return self.data_single('icon')

    @property
    def precipIntensity(self):
        """list: a list of precipitation amount."""
        return self.data_single('precipIntensity')
    
    @property
    def precipProbability(self):
        """list: a list precipitation probability in percentages."""
        return self.data_single('precipProbability', to_percent=True)

    @property
    def precipType(self):
        """list: a list of the type of precipitation."""
        return self.data_single('precipType')

    @property
    def dewPoint(self):
        """list: a list of dewpoints."""
        return self.data_single('dewPoint')

    @property
    def humidity(self):
        """list: a list of humidity in percentages."""
        return self.data_single('humidity', to_percent=True)
    
    @property
    def pressure(self):
        """list: a list of the air pressure."""
        return self.data_single('pressure')

    @property
    def windSpeed(self):
        """list: a list of wind speeds"""
        return self.data_single('windSpeed')

    @property
    def windGust(self):
        """list: a list of wind gusts"""
        return self.data_single('windGust')
    
    @property
    def windBearing(self):
        """list: a list of wind bearings."""
        return self.data_single('windBearing')

    @property
    def cloudCover(self):
        """list: a list of cloud coverage in percentage."""
        return self.data_single('cloudCover', to_percent=True)

    @property
    def uvIndex(self):
        """list: a list of uv indexes."""
        return self.data_single('uvIndex')

    @property
    def visibility(self):
        """list: a list of distance of visibility."""
        return self.data_single('visibility')
        
    @property
    def ozone(self):
        """list: a list of ozone levels."""
        return self.data_single('ozone')

    def __str__(self):
        return self.general_summary
    

class DSFCurrent:

    def __init__(self, data:dict):
        """Constructor method for Current class.

        Sets attributes automatically according to data["currently"].
         
        Arguments:
            data {dict} -- A dict containing the daily or hourly data from the DarkSkyAPI.
        """
        for k, v in data.items():
            setattr(self, k, v)
        logger.info(f"{repr(self)} created")

    def weekday(self, short:bool=False):
        """Gets the week day name for today
        
        Keyword Arguments:
            short {bool} -- Boolean to set days of the week to short or full (default: {False})
        
        Returns:
            str -- Week day name
        """
        if short:
            return timestamp(self.time, "%a")
        else:
            return timestamp(self.time, "%A")

    def is_raining(self):
        return self.precipProbability > 0

    def __str__(self):
        return f"Temperature: {self.temperature}\nSummary: {self.summary}\nPrecipitation probability: " \
                f"{int(self.precipProbability*100)}\nDay: {self.weekday()}"


class DSFDaily(DSFMBase):

    def __init__(self, data:dict):
        """Constructor method for Daily class.
        
        Sets attributes automatically according to data["daily"]. Inherits base attributes, methods and 
        properties from DSFMBase class.

        Arguments:
            data {dict} -- A dict containing the daily data from the DarkSkyAPI.
        """
        super().__init__(data)
        for index, item in enumerate(self.data):
            setattr(self, 'day_' + str(index), item)
    
    @property
    def temperatureHigh(self):
        """list: a list of daily max temperatures."""
        return self.data_single('temperatureHigh')

    @property
    def temperatureHighTime(self):
        """list: a list of daily max temperature times."""
        return self.data_single('temperatureHighTime', to_datetime=True)
    
    @property
    def apparentTemperatureHigh(self):
        """list: a list of daily apparent max temperatures."""
        return self.data_single('apparentTemperatureHigh')

    @property
    def apparentTemperatureHighTime(self):
        """list: a list of daily apparent max temperature times."""
        return self.data_single('apparentTemperatureHighTime', to_datetime=True)

    @property
    def temperatureLow(self):
        """list: a list of daily min temperatures."""
        return self.data_single('temperatureLow')

    @property
    def temperatureLowTime(self):
        """list: a list of daily min temperature times."""
        return self.data_single('temperatureLowTime', to_datetime=True)

    @property
    def apparentTemperatureLow(self):
        """list: a list of daily min apparent temperatures."""
        return self.data_single('apparentTemperatureLow')

    @property
    def apparentTemperatureLowTime(self):
        """list: a list of daily min apparent temperature times."""
        return self.data_single('apparentTemperatureLowTime', to_datetime=True)

    @property
    def sunriseTime(self):
        """list: a list of daily sunrise times."""
        return self.data_single('sunriseTime')
    
    @property
    def sunsetTime(self):
        """list: a list of daily sunset times."""
        return self.data_single('sunsetTime')

    @property
    def precipIntensityMax(self):
        """list: a list of daily max rain intensity."""
        return self.data_single('precipIntensityMax')

    @property
    def precipIntensityMaxTime(self):
        """list: a list of daily max rain intensity times."""
        return self.data_single('precipIntensityMaxTime', to_datetime=True)

    @property
    def moonPhase(self):
        """list: a list of daily moonphases."""
        return self.data_single('moonPhase')

    @property
    def windGustTime(self):
        """list: a list of daily wind gust times."""
        return self.data_single('windGustTime', to_datetime=True)

    @property
    def uvIndexTime(self):
        """list: a list of daily uv index times."""
        return self.data_single('uvIndexTime', to_datetime=True)
    

class DSFHourly(DSFMBase):

    def __init__(self, data:dict, hours:int=48):
        """Constructor method for Hourly class.
        
        Sets attributes automatically according to data["hourly"]. Inherits base attributes, methods and 
        properties from DSFMBase class.

        Arguments:
            data {dict} -- A dict containing the hourly data from the DarkSkyAPI.
        """
        super().__init__(data)
        for index, item in enumerate(self.data):
            setattr(self, 'hour_' + str(index), item)
    
    @property
    def temperature(self):
        """list: a list of hourly temperatures."""
        return self.data_single('temperature')

    @property
    def apparentTemperature(self):
        """list: a list of hourly apparent temperatures."""
        return self.data_single('apparentTemperature')


def timestamp(dt:int, fmt:str):
    """Helper function to convert timestamp to string
    
    Arguments:
        dt {int} -- timestamp
        fmt {str} -- datetime format
    
    Returns:
        str -- datetime string
    """
    return datetime.fromtimestamp(int(dt)).strftime(fmt)


def get_time_range(obj, t):
    """Helper function to choose time range based on instance of a class.
    
    Arguments:
        t {int} -- Amount of hours/days the user wants to return
    
    Returns:
        range -- range generator
    """
    if not t:
        if isinstance(obj, DSFDaily):
            time_range = range(0, 8)
            logger.info(f"{time_range} created for {repr(obj)}")
        else:
            time_range = range(0, 49)
            logger.info(f"{time_range} created for {repr(obj)}")
    else:
        time_range = range(0, t)
        logger.info(f"{time_range} created for {repr(obj)}")
    return time_range
