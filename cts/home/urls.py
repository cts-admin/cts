from django.conf.urls import url

from . import views

app_name = 'home'
urlpatterns = [
    url(r'^components/', views.components, name='components'),
***REMOVED***

***REMOVED***
    url(r'^index/', views.index, name='index'),
    url(r'^navbar/', views.navbar, name='navbar'),
    url(r'^notification/', views.notification, name='notification'),
    url(r'^template/', views.template, name='template'),
    url(r'^tutorial/', views.tutorial, name='tutorial'),
***REMOVED***