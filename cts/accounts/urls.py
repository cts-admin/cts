from django.conf.urls import include, url
from django_registration.views import RegistrationView

from django_registration.forms import RegistrationFormUniqueEmail

from . import views as account_views

urlpatterns = [
    url(
        r'^register/$',
        RegistrationView.as_view(form_class=RegistrationFormUniqueEmail),
        name='registration_register',
    ),
    url(
        r'^edit/$',
        account_views.edit_profile,
        name='edit_profile',
    ),
    url(r'', include('django_registration.backends.activation.urls')),
    url(r'', include('django.contrib.auth.urls')),
]
