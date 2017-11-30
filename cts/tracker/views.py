import os

from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from tracker.models import Waypoint

MAPS_API_KEY = os.environ.get('MAPS_API_KEY', None)


def index(request):
    waypoints = Waypoint.objects.all().order_by('name')
    return render_to_response('tracker/index.html', {
        'waypoints': waypoints,
        'maps_api_key': MAPS_API_KEY,
        'content': render_to_string('tracker/waypoints.html', {'waypoints': waypoints}),
    })
