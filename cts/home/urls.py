from django.conf.urls import url

from . import views

app_name = 'home'
urlpatterns = [
    url(r'^index/', views.index, name='index'),
***REMOVED***