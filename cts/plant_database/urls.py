from django.urls import path

from . import views

app_name = 'plant_database'
urlpatterns = [
    path('', views.index, name='index'),
    path('add-accession', views.add_accession, name='add_accession'),
]
