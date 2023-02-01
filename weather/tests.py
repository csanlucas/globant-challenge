from django.test import TestCase
from django.core.cache import cache
from django.conf import settings
from rest_framework import status

class WeatherApiTest(TestCase):
    ENDPOINT_URL = '/weather/'
    BOGOTA_CITY = 'Bogota'
    COLOMBIA_CODE = 'CO'
    ECUADOR_CODE = 'EC'
    SAMPLE_WEATHER_API_RESPONSE = {
        'location_name': 'test',
        'temperature_celsius': 'test',
        'temperature_fahrenheit': 'test',
        'wind': 'test',
        'cloudiness': 'test',
        'pressure': 'test',
        'humidity': 'test',
        'sunrise': 'test',
        'sunset': 'test',
        'geo_coordinates': 'test',
        'requested_time': 'test'
    }

    def test_not_allowed_request_methods(self):
        q_params = {'any1': 'tr', 'any2': 'tr'}
        self.assertTrue(self.client.post(self.ENDPOINT_URL, data=q_params).status_code == status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(self.client.delete(self.ENDPOINT_URL, data=q_params).status_code == status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(self.client.patch(self.ENDPOINT_URL, data=q_params).status_code == status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(self.client.put(self.ENDPOINT_URL, data=q_params).status_code == status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_required_valid_parameters(self):
        q_params = {'any1': 'tr', 'any2': 'tr'}
        req = self.client.get(self.ENDPOINT_URL, data=q_params)
        result = req.json()
        self.assertTrue(req.status_code == status.HTTP_400_BAD_REQUEST)
        self.assertTrue('error' in result)
    
    def test_invalid_country_city_params(self):
        q_params = {'city': 'sa78', 'country': 'ubeub34'}
        country_req = self.client.get(self.ENDPOINT_URL, data=q_params)
        country_result = country_req.json()
        q_params['country'] = 'ub'
        city_req = self.client.get(self.ENDPOINT_URL, data=q_params)
        city_result = city_req.json()
        self.assertTrue(country_req.status_code == status.HTTP_400_BAD_REQUEST)
        self.assertTrue('error' in country_result and 'country' in country_result['error'])
        self.assertTrue(city_req.status_code == status.HTTP_400_BAD_REQUEST)
        self.assertTrue('error' in city_result and 'city' in city_result['error'])
    
    def test_not_found_city(self):
        q_params = {'city': 'nanfcity', 'country': self.COLOMBIA_CODE}
        req = self.client.get(self.ENDPOINT_URL, data=q_params)
        result = req.json()
        self.assertTrue(req.status_code == status.HTTP_404_NOT_FOUND)
        self.assertTrue('message' in result and 'city' in result['message'])
    
    def test_not_found_city_on_country(self):
        q_params = {'city': self.BOGOTA_CITY, 'country': self.ECUADOR_CODE}
        req = self.client.get(self.ENDPOINT_URL, data=q_params)
        result = req.json()
        self.assertTrue(req.status_code == status.HTTP_404_NOT_FOUND)
        self.assertTrue('message' in result and 'city' in result['message'])
    
    def test_valid_query_weatherapi(self):
        q_params = {'city': self.BOGOTA_CITY, 'country': self.COLOMBIA_CODE}
        req = self.client.get(self.ENDPOINT_URL, data=q_params)
        result = req.json()
        self.assertTrue(req.status_code == status.HTTP_200_OK)
        self.assertTrue(set(self.SAMPLE_WEATHER_API_RESPONSE.keys()) == set(result.keys()))
    
    def test_cache_setup_done(self):
        self.assertTrue(settings.CACHES["default"]["BACKEND"] == 'django.core.cache.backends.db.DatabaseCache')
    
