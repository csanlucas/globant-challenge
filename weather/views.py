from datetime import datetime as dt
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
import re
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import WEATHER_PARTY_HOST, KELVIN_TO_CELSIUS, WEATHER_TTL_S, degreeToCompassLabel
from weatherapi.secrets import Config

class WeatheViewSet(APIView):

    @method_decorator(cache_page(WEATHER_TTL_S))
    @method_decorator(vary_on_cookie)
    def get(self, request):
        if not all(k in request.query_params for k in ("city", "country")):
            return Response({'error': 'Provide valid parameters'}, status=status.HTTP_400_BAD_REQUEST)
        country, city = request.query_params['country'], request.query_params['city']
        if not re.search("^([A-Za-z]{2})$", country):
            return Response({'error': 'Provide valid country code'}, status=status.HTTP_400_BAD_REQUEST)
        if not re.search("^([A-Za-z]*)$", city):
            return Response({'error': 'Provide valid city name'}, status=status.HTTP_400_BAD_REQUEST)
        w_req = requests.get(
            f"{WEATHER_PARTY_HOST}weather/",
            params= {
                'q': f"{city},{country}",
                'appid': Config.WEATHER_APPID
            },
            timeout=90)
        if w_req.status_code == 200:
            w_res = w_req.json()
            temp_celsius = round(w_res['main']['temp'] - KELVIN_TO_CELSIUS, 2)
            temp_fahrenheit = round(1.8 * temp_celsius + 32, 2)
            api_response = {
                'location_name': f"{city.title()}, {country.upper()}",
                'temperature_celsius': f"{temp_celsius} C",
                'temperature_fahrenheit': f"{temp_fahrenheit} F",
                'wind': f"{w_res['wind']['speed']} m/s, {degreeToCompassLabel(w_res['wind']['deg'])}",
                'cloudiness': f"{w_res['clouds']['all']} %",
                'pressure': f"{w_res['main']['pressure']} hpa",
                'humidity': f"{w_res['main']['humidity']}%",
                'sunrise': dt.fromtimestamp(w_res['sys']['sunrise'] + w_res['timezone']).strftime('%H:%M'),
                'sunset': dt.fromtimestamp(w_res['sys']['sunset'] + w_res['timezone']).strftime('%H:%M'),
                'geo_coordinates': f"[{w_res['coord']['lat']}, {w_res['coord']['lon']}]",
                'requested_time': dt.fromtimestamp(w_res['dt'] + w_res['timezone'])
            }
            return Response(data=api_response)
        else:
            return Response(status=w_req.status_code, data=w_req.json())
