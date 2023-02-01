WEATHER_PARTY_HOST = 'http://api.openweathermap.org/data/2.5/'

KELVIN_TO_CELSIUS = 273.15

WEATHER_TTL_S = 60*2

def degreeToCompassLabel(num):
    val=int((num/22.5)+.5)
    wind_direction=["North","North-northeast","Northeast","East-northeast","East",
        "East-southeast", "Southeast", "South-southeast","South","South-southwes","Southwest","West-southwest",
        "West","West-northwest","Northwest","North-northwest"]
    return wind_direction[(val % 16)]
