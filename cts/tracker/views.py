import os
import simplejson

from django.http import HttpResponse
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


def save(request):
    """
    Save waypoints.
    """
    for waypoint_str in request.POST.get('waypointsPayload', '').splitlines():
        waypoint_id, waypoint_x, waypoint_y = waypoint_str.split()
        waypoint = Waypoint.objects.get(id=int(waypoint_id))
        waypoint.geometry.set_x(float(waypoint_x))
        waypoint.geometry.set_y(float(waypoint_y))
        waypoint.save()

    return HttpResponse(simplejson.dumps(dict(isOk=1)), content_type='application/json')
