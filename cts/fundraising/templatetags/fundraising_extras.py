import datetime

from decimal import Decimal

from django import template
from django.conf import settings
from django.db import models
from django.template.defaultfilters import floatformat

from ..forms import DonateForm
from ..models import (
    DEFAULT_DONATION_AMOUNT, DISPLAY_DONOR_DAYS, GOAL_AMOUNT,
    LEADERSHIP_LEVEL_AMOUNT, CTSDonor, InKindDonor, Payment,
)
from members.models import (
    CORPORATE_MEMBERSHIP_AMOUNTS, CorporateMember, Invoice,
)

register = template.Library()


@register.filter
def as_percentage(part, total):
    if total is None or part is None:
        return "0.00"

    try:
        return floatformat((part / total) * Decimal("100.0"))
    except ZeroDivisionError:
        return "0.00"


@register.inclusion_tag('fundraising/includes/donation_form.html', takes_context=True)
def donation_form(context):
    user = context['user']
    goal_start = datetime.date(datetime.datetime.now().year, 1, 1)
    donated_amount = Payment.objects.filter(date__gte=goal_start).aggregate(
        models.Sum('amount'))['amount__sum'] or 0
    donated_amount += Invoice.objects.filter(paid_date__gte=goal_start).aggregate(
        models.Sum('amount'))['amount__sum'] or 0

    total_donors = CTSDonor.objects.filter(donation__payment__date__gte=goal_start).distinct().count()
    form = DonateForm(initial={
        'amount': DEFAULT_DONATION_AMOUNT,
    })

    return {
        'goal_amount': GOAL_AMOUNT,
        'goal_start_date': goal_start,
        'donated_amount': donated_amount,
        'total_donors': total_donors,
        'form': form,
        'display_logo_amount': LEADERSHIP_LEVEL_AMOUNT,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'user': user,
    }


@register.inclusion_tag('fundraising/includes/display_cts_donors.html')
def display_cts_donors():
    donors = CTSDonor.objects.for_public_display()
    i = 0
    for i, donor in enumerate(donors):
        if donor.donated_amount is not None and donor.donated_amount < LEADERSHIP_LEVEL_AMOUNT:
            break

    return {
        'corporate_members': CorporateMember.objects.by_membership_level(),
        'leaders': donors[:i],
        'donors': donors[i:],
        'inkind_donors': InKindDonor.objects.all(),
        'display_donor_days': DISPLAY_DONOR_DAYS,
        'display_logo_amount': int(LEADERSHIP_LEVEL_AMOUNT),
        'corporate_membership_amounts': CORPORATE_MEMBERSHIP_AMOUNTS,
    }
