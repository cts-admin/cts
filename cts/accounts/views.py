import hashlib
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileForm
from .models import Profile
from fundraising.models import CTSDonor


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get_or_create(user=user)
    donor = CTSDonor.objects.filter(profile=profile).first()
    if donor:
        donations = donor.donation_set.all()
    else:
        donations = None
    return render(request, "accounts/user_profile.html", {
        'user_obj': user,
        'email_hash': hashlib.md5(user.email.encode('ascii', 'ignore')).hexdigest(),
        'donor': donor,
        'donations': donations,
    })


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, instance=profile)
    if form.is_valid():
        form.save()
        return redirect('user_profile', request.user.username)
    return render(request, "accounts/edit_profile.html", {'form': form})


class JSONResponse(HttpResponse):
    def __init__(self, obj):
        super().__init__(
            json.dumps(obj, indent=(2 if settings.DEBUG else None)),
            content_type='application/json',
        )
