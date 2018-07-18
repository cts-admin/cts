import os
import tempfile
import json

from django.contrib.auth.decorators import login_required
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import Point
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from .models import Waypoint
from .forms import UploadFileForm

MAPS_API_KEY = os.environ.get('MAPS_API_KEY', None)


def add_marker(request):
    name = request.GET.get('name')
    marker_point = Point(float(request.GET.get('lng')), float(request.GET.get('lat')), srid=3857)
    waypoint = Waypoint(name=name, geometry=marker_point)
    waypoint.save()
    waypoints = Waypoint.objects.all()
    return HttpResponse(json.dumps(dict(
        content=render_to_string('tracker/waypoints.html', {
            'waypoints': waypoints
        }),
    )), content_type='application/json')


def index(request):
    form = UploadFileForm()
    waypoints = Waypoint.objects.all().order_by('name')
    return render(request, 'tracker/index.html', {
        'waypoints': waypoints,
        'maps_api_key': MAPS_API_KEY,
        'form': form,
        'content': render_to_string('tracker/waypoints.html', {'waypoints': waypoints}, request),
    })


def ol_index(request):
    return render(request, 'tracker/ol_index.html')


def load_pstz(request):
    with open('tracker/data/provision_seed_zones/psz_geojson.json') as infile:
        pstz_json = json.load(infile)
    return HttpResponse(json.dumps({
        'pstz': pstz_json,
    }))


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

    return HttpResponse(json.dumps(dict(isOk=1)), content_type='application/json')


def search(request):
    """
    Search waypoints.
    """
    try:
        search_point = Point(float(request.GET.get('lng')), float(request.GET.get('lat')), srid=3857)
    except:
        return HttpResponse(json.dumps(dict(isOk=0, message='Could not parse search point')))

    waypoints = Waypoint.objects.all().annotate(distance=Distance('geometry', search_point)).order_by('distance')
    return HttpResponse(json.dumps(dict(
        isOK=1,
        content=render_to_string('tracker/waypoints.html', {
            'waypoints': waypoints
        }),
        waypointByID=dict((x.id, {
            'name': x.name,
            'lat': x.geometry.y,
            'lng': x.geometry.x,
        }) for x in waypoints),
    )), content_type='application/json')


def handle_uploaded_file(file):
    target_path = tempfile.mkstemp()[1]
    with open(target_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    data_source = DataSource(target_path)
    layer = data_source[0]
    waypoint_names = layer.get_fields('name')
    waypoint_geometries = layer.get_geoms()
    for waypoint_name, waypoint_geometry in zip(waypoint_names, waypoint_geometries):
        waypoint = Waypoint(name=waypoint_name, geometry=waypoint_geometry.wkt)
        waypoint.save()
    os.remove(target_path)


@login_required(login_url='/accounts/login/')
def upload(request):
    """
    Upload waypoints from GPX file.
    """
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])

    return HttpResponseRedirect(reverse('tracker:index'))
