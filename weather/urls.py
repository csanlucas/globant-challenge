from django.urls import path
from .views import WeatheViewSet

url_locator = [
    path('weather/', WeatheViewSet.as_view())
]
