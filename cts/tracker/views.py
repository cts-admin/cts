import os

from django.shortcuts import render

MAPS_API_KEY = os.environ.get('MAPS_API_KEY', None)


def index(request):
    return render(request, 'tracker/index.html', {
        'maps_api_key': MAPS_API_KEY,
    })
