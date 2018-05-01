from django.urls import path

from . import views

urlpatterns = [
    path('hivecam/', views.hivecam, name='hivecam',
         ),
]
