from datetime import datetime


class DSFMBase:

    def __init__(self, data):
        self.data = data['data']
        self.summary = data['summary']
        self.icon = data['icon']
    
    def get_data(self, datapoint, date_fmt='%d-%m-%Y %H:%M', graph=False):
        if graph:
            return dict(x=[timestamp(i['time'], date_fmt) for i in self.data],
                        y=[i[datapoint] for i in self.data])
        else:
            return [(timestamp(i['time'], date_fmt), i[datapoint]) for i in self.data]


class DSFCurrent:

    def __init__(self, data):
        for k, v in data['currently'].items():
            setattr(self, k, v)


class DSFDaily(DSFMBase):

    def __init__(self, data):
        super().__init__(data)
        for index, item in enumerate(self.data):
            setattr(self, 'day_' + str(index), item)


class DSFHourly(DSFMBase):

    def __init__(self, data):
        super().__init__(data)
        for index, item in enumerate(self.data):
            setattr(self, 'hour_' + str(index), item)


def timestamp(dt, fmt):
    return datetime.fromtimestamp(int(dt)).strftime(fmt)
