from django.shortcuts import render, redirect
import requests
from .models import City, Info
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=2a5035a1a9287c44491f251ad0719454'
    extended = Info.objects.first()
    cities = City.objects.all()
    weather_data = []
    ex_weather_data = []
    form = CityForm()
    message = ''
    if request.method == 'POST':
        if 'city' in request.POST:
            form = CityForm(request.POST)
            if form.is_valid():
                temp = form.cleaned_data['name'].capitalize()
                x = City.objects.filter(name=temp).count()
                cod = requests.get(url.format(temp)).json()['cod']
                if x == 0 and cod != '404':
                    form.save()
                    message = 'City added.'
                elif x == 1:
                    message = 'City already loaded.'
                elif cod == '400':
                    message = 'Invalid city.'
        elif 'info' in request.POST:
            Info.objects.all().update(extended=not extended)
    extended = Info.objects.first()
    for city in cities:
        city_weather = requests.get(url.format(city)).json()
        weather = {
            'city': str(city).capitalize(),
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }
        weather_data.append(weather)
        ex_weather = {
            'city': str(city).capitalize(),
            'temperature': city_weather['main']['temp'],
            'feels_like': city_weather['main']['feels_like'],
            'pressure': city_weather['main']['pressure'],
            'humidity': city_weather['main']['humidity'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon'],
            'wind_speed': city_weather['wind']['speed']
        }
        ex_weather_data.append(ex_weather)
    context = {
        'weather_data': weather_data,
        'ex_weather_data': ex_weather_data,
        'form': form,
        'message': message,
        'extended': extended
    }
    return render(request, 'weatherApp/index.html', context)


def delete(request, name):
    City.objects.all().filter(name=name).delete()
    return redirect('main')
