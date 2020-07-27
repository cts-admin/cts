from django.conf import settings
from django.conf.urls import url
from django.urls import path

from . import views
# Needed to actually load the dash app
from . import dash_app

app_name = 'home'
urlpatterns = [
    url(r'^contact/', views.contact, name='contact'),
    url(r'^mission/', views.mission, name='mission'),
    path('demo-six/', views.dash_example_1_view, name="demo-six"),
    url(r'^$', views.home, name='home'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^index/', views.index, name='index'),
        url(r'^components/', views.components, name='components'),
        url(r'^navbar/', views.navbar, name='navbar'),
        url(r'^notification/', views.notification, name='notification'),
        url(r'^template/', views.template, name='template'),
        url(r'^tutorial/', views.tutorial, name='tutorial'),
    ]
