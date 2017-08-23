from django.conf.urls import include, url
from registration.backends.model_activation.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail

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
    url(r'', include('django.contrib.auth.urls')),
    url(r'', include('registration.backends.default.urls')),
]