from django.shortcuts import render
from django.http import JsonResponse
import requests
import os
from datetime import datetime

def index(request):
    return render(request, 'my_weather_app/index.html')

def search_weather(request):
    if request.method == 'POST':
        city_name = request.POST.get('city_name')
        # Fetch weather data
        weather_data = get_weather_data(city_name)
        return JsonResponse(weather_data, safe=False)
    return render(request, 'my_weather_app/index.html')

def get_weather_data(city_name):
    # Geocoding API call
    lat, lon = get_coordinates(city_name)
    # Current weather API call
    current_weather = get_current_weather(lat, lon)
    # Cache data
    cache_data(city_name, lat, lon, current_weather)
    return current_weather

def get_coordinates(city_name):
    # API call to get latitude and longitude
    geocoding_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={os.getenv("OPEN_WEATHER_API_KEY")}'
    response = requests.get(geocoding_url)
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    return None, None

def get_current_weather(lat, lon):
    # API call to get current weather
    current_weather_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={os.getenv("OPEN_WEATHER_API_KEY")}&units=metric'
    response = requests.get(current_weather_url)
    data = response.json()
    return data

def cache_data(city_name, lat, lon, data):
    # Cache data to a file
    filename = f'{city_name}-{lat}-{lon}.txt'
    with open(filename, 'w') as file:
        file.write(str(data))

def is_data_expired(filename):
    # Check if data is older than 180 minutes
    if os.path.exists(filename):
        modified_time = os.path.getmtime(filename)
        current_time = datetime.now().timestamp()
        if (current_time - modified_time) > 10800:  # 180 minutes
            return True
    return False

def get_cached_data(city_name, lat, lon):
    # Get cached data
    filename = f'{city_name}-{lat}-{lon}.txt'
    if not is_data_expired(filename):
        with open(filename, 'r') as file:
            return eval(file.read())
    return None