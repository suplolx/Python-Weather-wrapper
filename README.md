# Python-Weather-wrapper
API wrapper for DarkSkyAPI written in Python 3.6.5. Powered by https://darksky.net/poweredby/

### Usage examples

#### Creating the client instance.
```python
from DarkSkyAPI import DarkSkyClient

api_key = YOUR_API_KEY

client = DarkSkyClient(api_key, lat=37.423021, lon=-122.083739)
```

#### Getting current weather details
All weather details are available like attributes using dot notation.
```python
# Creating current instance
current = client.get_current()

print(f"Current temperature: {current.temperature}")
print(f"Feels like: {current.apparentTemperature}")
```

#### Getting daily forecast details for next 7 days
Daily weather details are both available using the day_n attribute followed by the datapoint and by using the raw data object for looping.
```python
# Creating daily forecast instance
daily = client.get_daily()

# Individual 
print(f"Max temperature today: {daily.day_0['temperatureHigh']}")
print(f"Max temperature today: {daily.day_0['temperatureLow']}")

# Raw data
for item in daily.data:
    print(f"Max temperature: {item['temperatureHigh']}")
    print(f"Min temperature: {item['temperatureLow']}")
```

#### Getting hourly forecast details for next 48 hours
Hourly weather details are both available using the hour_n attribute followed by the datapoint and by using the raw data object for looping.
```python
# Creating hourly instance
hourly = client.get_hourly()

# Individual 
print(f"Probability of rain: {hourly.hour_0['precipProbability']}")
print(f"Amount of rain (mm/h): {hourly.hour_0['precipIntensity']}")

# Raw data
for item in hourly.data:
    print(f"Probability of rain: {item['precipProbability']}")
    print(f"Amount of rain (mm/h): {item['precipIntensity']}")
```

#### Retrieving a list of value pair tuples containing the maximum temperature for each day.
The first item in the tuple represents the day and the second item represents the value
```python
max_temps = daily.data_pair('temperatureHigh')

Out[]:
[('28-05-2018 00:00', 29.62),
 ('29-05-2018 00:00', 26.08),
 ('30-05-2018 00:00', 27.66),
 ('31-05-2018 00:00', 26.66),
 ('01-06-2018 00:00', 27.04),
 ('02-06-2018 00:00', 28.22),
 ('03-06-2018 00:00', 29.34),
 ('04-06-2018 00:00', 29.01)]
```
If you want to use a different datetime format you can pass your own format using the date_fmt parameter
```python
max_temps = daily.data_pair('temperatureHigh', date_fmt="%A")  

Out[]:
[('Monday', 29.62),
 ('Tuesday', 26.08),
 ('Wednesday', 27.66),
 ('Thursday', 26.66),
 ('Friday', 27.04),
 ('Saturday', 28.22),
 ('Sunday', 29.34),
 ('Monday', 29.01)]
```
You can make the data friendlier to use in graphs by settings the graph paramter to True
```python
max_temps = daily.data_pair('temperatureHigh', graph=True)

Out[]:
{'x': ['28-05-2018 00:00', '29-05-2018 00:00', '30-05-2018 00:00', '31-05-2018 00:00', '01-06-2018 00:00', '02-06-2018 00:00', '03-06-2018 00:00', '04-06-2018 00:00'],
 'y': [29.62, 26.08, 27.66, 26.66, 27.04, 28.22, 29.34, 29.01]}
```
This method is also available on the daily object.
