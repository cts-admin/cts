from django.conf import settings
from django.conf.urls import url

from . import views

app_name = 'home'
urlpatterns = [
    url(r'^contact/', views.contact, name='contact'),
    url(r'^mission/', views.mission, name='mission'),
    url(r'^$', views.home, name='home'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^index/', views.index, name='index'),
        url(r'^navbar/', views.navbar, name='navbar'),
        url(r'^notification/', views.notification, name='notification'),
        url(r'^template/', views.template, name='template'),
        url(r'^tutorial/', views.tutorial, name='tutorial'),
    ]
