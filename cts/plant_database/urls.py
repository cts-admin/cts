from django.urls import path

from . import views

app_name = 'plant_database'
urlpatterns = [
    path('', views.index, name='index'),
    path('add-seed-accession', views.add_seed_accession, name='add_seed_accession'),
]
