# DarkSkyAPI wrapper
The DarkSkyAPI weather wrapper is [powered by DarkSky](https://darksky.net/poweredby/) and provides an easy way to access weather details using Python 3.6.

## Install
```
pip install darkskyapi-py
```

## Usage

### Client instance
First import the DarkSkyClient class from the DarkSkyAPI module. If you don't have an API key for the DarkSkyAPI yet, get one for free [here](https://darksky.net/dev/register). This will allow you to make a 1000 calls each day.

```python
from DarkSkyAPI.DarkSkyAPI import DarkSkyClient
```
Next, create the client instance using the api_key as the first argument and a tuple containing the latitude and longitude of the location as the second argument. The third argument is optional and will set the units (Celsius/Fahrenheit). The unit options are as follows:

* auto: automatically select units based on geographic location
* ca: same as si, except that windSpeed and windGust are in kilometers per hour
* uk2: same as si, except that nearestStormDistance and visibility are in miles, and windSpeed and windGust in miles per hour.
* us: Imperial units
* si: International System of Units (default)
If no units are provided it will default to "si".
```python
client = DarkSkyClient(api_key, (lat, lon), units="si")
```
The client instance already holds the raw weather response and can be accessed by client.raw_data.
```python
client.raw_data
```
Additionally it also keeps track of the remaining api calls for the current day.
```python
client.API_calls_remaining
```
### Current instance
To create the current instance, simply call the get_current method on client.

```python
current = client.get_current()
```
All the data points of the current weather details are automatically set as attributes of the instance. This allows you to use the datapoints like attributes.

```python
current.temperature
```
The weekday can be accessed by calling the weekday attribute on the current instance. This will return the full weekday name (in English). To return the short weekday name (i.e Mon, Tue), use the weekday_short attribute.
```python
current.weekday
current.weekday_short
```

### Daily and hourly instance
To create the daily and hourly instance, simply call the get_daily and get_hourly method on client.

```python
daily = client.get_daily()
hourly = client.get_hourly()
```
To customize the amount of hours or days are returned, simply pass the n amount of hours/days as an int to the method.

```python
# Returns 5 days (including today)
daily = client.get_daily(6)
# Returns 24 hours (including current hour)
hourly = client.get_hourly(24)
```
The daily and hourly classes behave in the same way because they inherit from the same base class. Because of this, only the daily instance is documented. The terms hourly/daily and hour/day can be used interchangeably.

The forecast datapoints can be accessed in various ways. To get the data by individual days or hours you can either use the day/hour_n attribute or the data list of the forecast instance.

```python
# Day attribute
daily.day_0['temperatureHigh']

# Daily data list
daily.data[0]['temperatureHigh']
```
Both instances also have every date point set as a property. These properties hold a list of single datapoint values.
```python
daily.temperatureHigh
```

Alternatively, there are several methods you can use to get data collections of one or more datapoints. These methods work on both the daily and hourly instance. The methods currently available are:

* data_pair: Will return a list of value pair tuples containing firstly the datetime and secondly the value of the datapoint. This method accepts three arguments. The first argument is the datapoint (required). The second argument is the date_fmt parameter and will set the format of the datetime value (default - "%d-%m-%Y %H:%M"). The third argument is the graph argument, if set to True it wil return a graph-friendly dict of the datetime and values of the datapoint (default - False).
* data_single: Will return a list of single datapoint values. This method accepts three arguments. The first argument is the datapoint you wan the values of. The second argument is a boolean that will convert the datapoint to percentages if set to True (default: False). The third argument is a boolean that will convert the datapoint to a datetime string if set to True (default: False).
* data_combined: Will return a dict containing lists of datapoint values for each day/hour. This method accepts two arguments. The first is the list of datapoints. The second is the date_fmt incase the datapoint is time. If you don't provide a list of datapoints it will return all datapoints. 
* datetimes: Will return a list containing all the datetimes of the days/hours. This method accepts one argument which is the dateformat (default - "%d-%m-%Y %H:%M")
#### Data pair method
```python
# Data pair default date format and no graph
daily.data_pair('temperatureHigh')

# Data pair weekday names date_fmt
daily.data_pair('temperatureHigh', date_fmt="%A")

# Data pair graph
daily.data_pair('temperatureHigh', graph=True)
```
#### Data single method
```python
# Datapoint argument.
daily.data_single('temperatureHigh')

# Datapoint argument and to_percent argument set to True.
daily.data_single('precipProbability', to_percent=True)

# Datapoint argument and to_datetime argument set to True.
daily.data_single('precipIntensityMaxTime', to_datetime=True)
```
#### Data combined method
```python
# Specified list of datapoints
daily.data_combined(['temperatureHigh', 'temperatureLow'], date_fmt="%H:%M")

# All data points
daily.data_combined()
```
#### Datetimes method
```python
# Default date format
daily.datetimes()

# Weekday names date format (short)
daily.datetimes(date_fmt="%a")
```
