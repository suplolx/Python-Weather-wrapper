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
