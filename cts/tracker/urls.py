from django.conf.urls import url

from . import views

app_name = 'tracker'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ol$', views.ol_index, name='ol_index'),
    url(r'^save$', views.save, name='save'),
    url(r'^search$', views.search, name='search'),
    url(r'^upload$', views.upload, name='upload'),
    url(r'^ajax/add-marker$', views.add_marker, name='add_marker'),
]
