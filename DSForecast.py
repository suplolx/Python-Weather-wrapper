from datetime import datetime


class DSFCurrent:

    def __init__(self, data):
        for k, v in data['currently'].items():
            setattr(self, k, v)


class DSFDaily:

    date_fmt = "%d-%m-%Y"

    def __init__(self, data):
        self.day_summary = data['daily']['summary']
        self.icon = data['daily']['icon']
        self.data = data['daily']['data']
        self.precipProbability = self.get_data('precipProbability')
        self.icon = self.get_data('icon')
        self.temperatureMax = self.get_data('temperatureHigh')
        self.temperatureMin = self.get_data('temperatureLow')
        self.humidity = self.get_data('humidity')
        self.windSpeed = self.get_data('windSpeed')
        self.summary = self.get_data('summary')
        for index, item in enumerate(self.data):
            setattr(self, 'day_' + str(index), item)

    def get_data(self, datapoint, weekday='long'):
        if weekday == 'long':
            return [(timestamp(i['time'], '%A'), i[datapoint]) for i in self.data]
        elif weekday == 'short':
            return [(timestamp(i['time'], '%a'), i[datapoint]) for i in self.data]
        elif weekday == 'date':
            return [(timestamp(i['time'], self.date_fmt), i[datapoint]) for i in self.data]
        else:
            return None
    
    @staticmethod
    def to_graph(data_list):
        return dict(x=[i[0] for i in data_list],
                    y=[i[1] for i in data_list])


class DSFHourly:

    date_fmt = "%d-%m-%Y %H:%M"

    def __init__(self, data):
        self.hour_summary = data['hourly']['summary']
        self.icon = data['hourly']['icon']
        self.data = data['hourly']['data']
        self.summary = self.get_data('summary')
        self.temperature = self.get_data('temperature')
        self.precipProbability = self.get_data('precipProbability')
        self.precipIntensity = self.get_data('precipIntensity')
        self.humidity = self.get_data('humidity')
        self.windSpeed = self.get_data('windSpeed')
        for index, item in enumerate(self.data):
            setattr(self, 'hour_' + str(index), item)

    def get_data(self, datapoint):
        return [(timestamp(i['time'], self.date_fmt), i[datapoint]) for i in self.data]

    @staticmethod
    def to_graph(data_list):
        return dict(x=[i[0] for i in data_list],
                    y=[i[1] for i in data_list])


def timestamp(dt, fmt):
    return datetime.fromtimestamp(int(dt)).strftime(fmt)
