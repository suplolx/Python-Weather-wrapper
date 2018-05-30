from datetime import datetime


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
    
    def data_pair(self, datapoint:str, date_fmt:str='%d-%m-%Y %H:%M', graph:bool=False):
        """Generates a list of value pairs containing datetimes and datapoint values.

        Arguments:
            datapoint {str} -- The forecast datapoint you want the values from (example: windSpeed)
        
        Keyword Arguments:
            date_fmt {str} -- The datetime format (default: {'%d-%m-%Y %H:%M'})
            graph {bool} --  a graph-friendly dict (default: {False})
        
        Returns:
            list -- list of tuple value pairs
            dict -- graph-friendly dict when graph set to True 
        """
        if graph:
            return dict(x=[timestamp(i['time'], date_fmt) for i in self.data],
                        y=[i[datapoint] for i in self.data])
        else:
            return [(timestamp(i['time'], date_fmt), i[datapoint]) for i in self.data]
    
    def data_single(self, datapoint:str, to_percent=False, to_datetime=False):
        """Generates a list of single datapoint values.
        
        Arguments:
            datapoint {str} -- The forecast datapoint you want the values of (example: windSpeed)
        
        Returns:
            list -- A list containing single datapoint values
        """
        if to_percent:
            return [i[datapoint] * 100 if datapoint in i else None for i in self.data]
        elif to_datetime:
            return [timestamp(i[datapoint], "%d-%m-%Y %H:%M") if datapoint in i else None for i in self.data]
        else:
            return [i[datapoint] if datapoint in i else None for i in self.data]

    def data_combined(self, datalist:list=None):
        """Generates a custom dict of datapoint values for each day/hour.

        Keyword Arguments:
            datalist {list} -- A list of datapoints you want the values of (default: {None})
        
        Returns:
            dict -- A dict of datapoints and their corresponding values. If no list is provided, all datapoints will  be used.
        """
        if datalist:
            return {datapoint: [i[datapoint] for i in self.data] for datapoint in datalist}
        else:
            datalist = [datakey for datakey in self.data[0].keys()]
            return {datapoint: [i.get(datapoint, None) for i in self.data] for datapoint in datalist}

    def datetimes(self, date_fmt:str="%d-%m-%Y %H:%M"):
        """Generates a list of datetime strings of all the hours/days
        
        Keyword Arguments:
            date_fmt {str} -- The datetime format (default: {"%d-%m-%Y %H:%M"})
        
        Returns:
            list -- A list of datetime strings of all the hours/days
        """
        return [timestamp(i['time'], date_fmt) for i in self.data]

    @property
    def time(self):
        """list: a list of datetime strings"""
        return self.data_single('time', to_datetime=True)
    
    @property
    def summary(self):
        """list: a list of weather summary's"""
        return self.data_single('summary')

    @property
    def icon(self):
        """list: a list of weather icons"""
        return self.data_single('icon')

    @property
    def precipIntensity(self):
        return self.data_single('precipIntensity')
    
    @property
    def precipProbability(self):
        return self.data_single('precipProbability', to_percent=True)

    @property
    def precipType(self):
        return self.data_single('precipType')

    @property
    def dewPoint(self):
        return self.data_single('dewPoint')

    @property
    def humidity(self):
        return self.data_single('humidity', to_percent=True)
    
    @property
    def pressure(self):
        return self.data_single('pressure')

    @property
    def windSpeed(self):
        return self.data_single('windSpeed')

    @property
    def windGust(self):
        return self.data_single('windGust')
    
    @property
    def windBearing(self):
        return self.data_single('windBearing')

    @property
    def cloudCover(self):
        return self.data_single('cloudCover', to_percent=True)

    @property
    def uvIndex(self):
        return self.data_single('uvIndex')

    @property
    def visibility(self):
        return self.data_single('visibility')
        
    @property
    def ozone(self):
        return self.data_single('ozone')
    

class DSFCurrent:

    def __init__(self, data:dict):
        for k, v in data.items():
            setattr(self, k, v)

    def weekday(self, short:bool=False):
        if short:
            return timestamp(self.time, "%a")
        else:
            return timestamp(self.time, "%A")


class DSFDaily(DSFMBase):

    def __init__(self, data:dict):
        super().__init__(data)
        for index, item in enumerate(self.data):
            setattr(self, 'day_' + str(index), item)
    
    @property
    def temperatureHigh(self):
        return self.data_single('temperatureHigh')

    @property
    def temperatureHighTime(self):
        return self.data_single('temperatureHighTime', to_datetime=True)
    
    @property
    def apparentTemperatureHigh(self):
        return self.data_single('apparentTemperatureHigh')

    @property
    def apparentTemperatureHighTime(self):
        return self.data_single('apparentTemperatureHighTime', to_datetime=True)

    @property
    def temperatureLow(self):
        return self.data_single('temperatureLow')

    @property
    def temperatureLowTime(self):
        return self.data_single('temperatureLowTime', to_datetime=True)

    @property
    def apparentTemperatureLow(self):
        return self.data_single('apparentTemperatureLow')

    @property
    def apparentTemperatureLowTime(self):
        return self.data_single('apparentTemperatureLowTime', to_datetime=True)

    @property
    def sunriseTime(self):
        return self.data_single('sunriseTime')
    
    @property
    def sunsetTime(self):
        return self.data_single('sunsetTime')

    @property
    def precipIntensityMax(self):
        return self.data_single('precipIntensityMax')

    @property
    def precipIntensityMaxTime(self):
        return self.data_single('precipIntensityMaxTime', to_datetime=True)

    @property
    def moonPhase(self):
        return self.data_single('moonPhase')

    @property
    def windGustTime(self):
        return self.data_single('windGustTime', to_datetime=True)

    @property
    def uvIndexTime(self):
        return self.data_single('uvIndexTime', to_datetime=True)
    

class DSFHourly(DSFMBase):

    def __init__(self, data:dict):
        super().__init__(data)
        for index, item in enumerate(self.data):
            setattr(self, 'hour_' + str(index), item)
    
    @property
    def temperature(self):
        return self.data_single('temperature')

    @property
    def apparentTemperature(self):
        return self.data_single('apparentTemperature')


def timestamp(dt:int, fmt:str):
    return datetime.fromtimestamp(int(dt)).strftime(fmt)
