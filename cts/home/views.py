from django.shortcuts import render


# Testing out the Get Shit Done bootstrap package
def index(request):
    return render(request, 'home/index.html')


def components(request):
    return render(request, 'home/components.html')


def navbar(request):
    return render(request, 'home/navbar-transparent.html')


def notification(request):
    return render(request, 'home/notification.html')


def template(request):
    return render(request, 'home/template.html')


def tutorial(request):
    return render(request, 'home/tutorial.html')
