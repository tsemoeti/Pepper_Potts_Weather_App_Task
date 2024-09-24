from django.urls import path
from .views import search_weather, index

urlpatterns = [
    path('', index, name='index'),  # Root URL
    path('search/', search_weather, name='search_weather'),
]