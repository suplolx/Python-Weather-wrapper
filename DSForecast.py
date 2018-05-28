from datetime import datetime


class DSFMBase:

    def __init__(self, data:dict):
        self.data = data['data']
        self.summary = data['summary']
        self.icon = data['icon']
    
    def data_pair(self, datapoint:str, date_fmt:str='%d-%m-%Y %H:%M', graph:bool=False):
        if graph:
            return dict(x=[timestamp(i['time'], date_fmt) for i in self.data],
                        y=[i[datapoint] for i in self.data])
        else:
            return [(timestamp(i['time'], date_fmt), i[datapoint]) for i in self.data]
    
    def data_single(self, datapoint:str):
        return [i[datapoint] for i in self.data]

    def data_combined(self, datalist:list=None):
        if datalist:
            return {datapoint: [i[datapoint] for i in self.data] for datapoint in datalist}
        else:
            datalist = [datakey for datakey in self.data[0].keys()]
            return {datapoint: [i.get(datapoint, None) for i in self.data] for datapoint in datalist}

    def datetimes(self, date_fmt:str="%d-%m-%Y %H:%M"):
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
