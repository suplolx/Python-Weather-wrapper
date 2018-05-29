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
        self.summary = data['summary']
        self.icon = data['icon']
    
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
    
    def data_single(self, datapoint:str):
        """Generates a list of single datapoint values.
        
        Arguments:
            datapoint {str} -- The forecast datapoint you want the values of (example: windSpeed)
        
        Returns:
            list -- A list containing single datapoint values
        """
        return [i[datapoint] for i in self.data]

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


class DSFHourly(DSFMBase):

    def __init__(self, data:dict):
        super().__init__(data)
        for index, item in enumerate(self.data):
            setattr(self, 'hour_' + str(index), item)


def timestamp(dt:int, fmt:str):
    return datetime.fromtimestamp(int(dt)).strftime(fmt)
