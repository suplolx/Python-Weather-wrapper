# DarkSkyAPI wrapper
The DarkSkyAPI weather wrapper is [powered by DarkSky](https://darksky.net/poweredby/) and provides an easy way to access weather details using Python 3.6.

## Client instance
First import the DarkSkyClient class from the DarkSkyAPI module. If you don't have an API key for the DarkSkyAPI yet, get one for free [here](https://darksky.net/dev/register). This will allow you to make a 1000 calls each day.

```python
from DarkSkyAPI import DarkSkyClient
```
Next, create the client instance using the api_key as the first argument and the latitude-longitude of the location as the second and third argument. The fourth argument is optional and will set the units (Celsius/Fahrenheit). The unit options are as follows:

* auto: automatically select units based on geographic location
* ca: same as si, except that windSpeed and windGust are in kilometers per hour
* uk2: same as si, except that nearestStormDistance and visibility are in miles, and windSpeed and windGust in miles per hour.
* us: Imperial units
* si: International System of Units (default)
If no units are provided it will default to "si". Both lat and lon can either be floats or strings.
```python
client = DarkSkyClient(api_key, lat, lon, units="si")
```
The client instance already holds the raw weather response and can be accessed by client.raw_data.
```python
client.raw_data
```
Additionally, it also holds the timezone.
```python
client.timezone
```
## Current instance
To create the current instance, simply call the get_current method on client.

```python
current = client.get_current()
```
All the data points of the current weather details are automatically set as attributes of the instance. This allows you to use the datapoints like attributes.

```python
current.temperature
```
The weekday can be accessed by calling the weekday method on the current instance. This will return the full weekday name (in English). To return the short weekday name (i.e Mon, Tue), set the short parameter to True.
```python
current.weekday()
current.weekday(short=True)
```

## Daily and hourly instance
To create the daily and hourly instance, simply call the get_daily and get_hourly method on client.

```python
daily = client.get_daily()
hourly = client.get_hourly()
```
The daily and hourly classes behave in the same way because they inherit from the same base class. Because of this, only the daily instance is documented. The terms hourly/daily and hour/day can be used interchangeably.

The forecast datapoints can be accessed in various ways. To get the data by individual days or hours you can either use the day/hour_n attribute or the data list of the forecast instance.

```python
# Day attribute
daily.day_0['temperatureHigh']

# Daily data list
daily.data[0]['temperatureHigh']
```
Alternatively, there are several methods you can use to get data collections of one or more datapoints. These methods work on both the daily and hourly instance. The methods currently available are:

* data_pair(datapoint, date_fmt, graph): Will return a list of value pair tuples containing firstly the datetime and secondly the value of the datapoint. This method accepts three arguments. The first argument is the datapoint (required). The second argument is the date_fmt parameter and will set the format of the datetime value (default - "%d-%m-%Y %H:%M"). The third argument is the graph argument, if set to True it wil return a graph-friendly dict of the datetime and values of the datapoint (default - False).
* data_single(datapoint): Will return a list of single data values. This method accepts one method which is the datapoint.
* data_combined(datalist): Will return a dict containing lists of datapoint values for each day/hour. This method accepts one argument which is the list of datapoints you want to retrieve. If you don't provide an argument it will return all datapoints.
* datetimes(date_fmt): Will return a list containing all the datetimes of the days/hours. This method accepts one argument which is the dateformat (default - "%d-%m-%Y %H:%M")
### Data pair method
```python
# Data pair default date format and no graph
daily.data_pair('temperatureHigh')

# Data pair weekday names date_fmt
daily.data_pair('temperatureHigh', date_fmt="%A")

# Data pair graph
daily.data_pair('temperatureHigh', graph=True)
```
### Data single method
```python
daily.data_single('temperatureHigh')
```
### Data combined method
```python
# Specified list of datapoints
daily.data_combined(['temperatureHigh', 'temperatureLow'])

# All data points
daily.data_combined()
```
### Datetimes method
```python
# Default date format
daily.datetimes()

# Weekday names date format (short)
daily.datetimes(date_fmt="%a")
```
