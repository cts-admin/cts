from django.shortcuts import render


def index(request):
    return render(request, 'plant_database/index.html')
