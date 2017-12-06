from django.conf.urls import url

from . import views

app_name = 'tracker'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^save$', views.save, name='save'),
    url(r'^search$', views.search, name='search'),
    url(r'^upload$', views.upload, name='upload'),
    url(r'^load_pstz$', views.load_pstz, name='load_pstz'),
]
