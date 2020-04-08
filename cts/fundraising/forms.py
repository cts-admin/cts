import stripe
from django import forms
from django.conf import settings
from django.db import IntegrityError
from django.forms.widgets import Select
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from .exceptions import DonationError
from .models import (
    INTERVAL_CHOICES, LEADERSHIP_LEVEL_AMOUNT, CTSDonor, Donation,
)
from accounts.models import Profile

from home.tasks import mail_task


class CTSDonorForm(forms.ModelForm):
    donor_type = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect(attrs={'data-toggle': 'radio'}),
        label='I am donating as an',
        choices=CTSDonor.DONOR_TYPE_CHOICES,
    )
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'required form-control',
                'placeholder': 'Your name or the name of your organization',
            },
        )
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Where are you located? (optional; will not be displayd)',
            },
        )
    )
    url = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Which URL should we link your name to?',
            },
        )
    )
    logo = forms.FileField(
        required=False,
        help_text=(
            "If you've donated at least US $%d, you can submit your logo and "
            "we will display it, too." % LEADERSHIP_LEVEL_AMOUNT
        ),
    )
    is_visible = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'data-toggle': 'checkbox'}
        ),
        label=(
            "Yes, display my name, URL, and logo on this site. "
            "It'll be displayed shortly after we verify it."
        ),
    )
    is_subscribed = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'data-toggle': 'checkbox'}
        ),
        label=(
            'Yes, Conservation Technology Solutions Inc can inform me about '
            'future fundraising campaigns by email.'
        ),
    )

    class Meta:
        model = CTSDonor
        fields = (
            'donor_type', 'name', 'location', 'url', 'logo', 'is_visible',
            'is_subscribed',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checkbox_fields = []
        self.radio_select_fields = []

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                self.checkbox_fields.append(name)
            elif isinstance(field.widget, forms.RadioSelect):
                self.radio_select_fields.append(name)

    def save(self, commit=True):
        donor = super().save(commit=commit)
        customer = stripe.Customer.retrieve(donor.stripe_customer_id)
        customer.description = donor.name or None
        customer.email = donor.email or None
        customer.save()
        return donor


class StripeTextInput(forms.TextInput):
    """
    Inspired by widgets in django-zebra
    """
    def _add_data_stripe_attr(self, name, kwargs):
        kwargs.setdefault('attrs', {}).update({'data-stripe': name})
        return kwargs

    def _strip_name_attr(self, widget_string, name):
        return widget_string.replace("name=\"%s\"" % (name,), "")

    def render(self, name, *args, **kwargs):
        kwargs = self._add_data_stripe_attr(name, kwargs)
        rendered = super().render(name, *args, **kwargs)
        return mark_safe(self._strip_name_attr(rendered, name))


class DonateForm(forms.Form):
    AMOUNT_CHOICES = (
        (5, 'US $5'),
        (10, 'US $10'),
        (25, 'US $25'),
        (50, 'US $50'),
        (100, 'US $100'),
        (250, 'US $250'),
        ('custom', 'Other amount'),
    )

    amount = forms.ChoiceField(choices=AMOUNT_CHOICES, widget=Select(attrs={'class': 'form-group form-control'}))
    interval = forms.ChoiceField(choices=INTERVAL_CHOICES, widget=Select(attrs={'class': 'form-group form-control'}))


class DonationForm(forms.ModelForm):
    subscription_amount = forms.DecimalField(max_digits=9, decimal_places=2, required=True,
                                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    # here we're removing "onetime" option from interval choices:
    interval = forms.ChoiceField(choices=INTERVAL_CHOICES[:3], required=True,
                                 widget=Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Donation
        fields = ('subscription_amount', 'interval')

    def save(self, commit=True, *args, **kwargs):
        donation = super().save(commit=commit)
        interval = self.cleaned_data.get('interval')
        amount = self.cleaned_data.get('subscription_amount')

        # Send data to Stripe
        customer = stripe.Customer.retrieve(donation.stripe_customer_id)
        subscription = customer.subscriptions.retrieve(donation.stripe_subscription_id)
        subscription.plan = interval
        subscription.quantity = int(amount)
        subscription.save()

        return donation


class PaymentForm(forms.Form):
    amount = forms.IntegerField(
        required=True,
        min_value=1,  # Minimum payment from Stripe API
    )
    interval = forms.ChoiceField(
        required=True,
        choices=INTERVAL_CHOICES,
    )
    receipt_email = forms.CharField(required=True)
    # added by the donation form JavaScript via Stripe.js
    stripe_token = forms.CharField(widget=forms.HiddenInput())
    token_type = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PaymentForm, self).__init__(*args, **kwargs)

    def make_donation(self):
        receipt_email = self.cleaned_data['receipt_email']
        amount = self.cleaned_data['amount']
        stripe_token = self.cleaned_data['stripe_token']
        token_type = self.cleaned_data['token_type']
        interval = self.cleaned_data['interval']
        is_bitcoin = token_type == 'source_bitcoin'
        user = self.user

        donor = CTSDonor.objects.filter(email=receipt_email).first() or \
                CTSDonor.objects.filter(email=user.email).first()

        try:
            if donor and donor.stripe_customer_id:
                # Update old customer with new payment source, unless the
                # source is bitcoin.
                customer = stripe.Customer.retrieve(donor.stripe_customer_id)
                if is_bitcoin:
                    customer.sources.create(source=stripe_token)
                else:
                    customer.source = stripe_token
                customer.save()
            else:
                customer = stripe.Customer.create(source=stripe_token, email=receipt_email)

            # Only perform one-time charges with bitcoin as bitcoins can't be
            # used for subscriptions.
            if interval == 'onetime' or is_bitcoin:
                subscription_id = ''
                charge_info = {
                    'amount': int(amount * 100),
                    'currency': 'usd',
                    'customer': customer.id,
                    'receipt_email': receipt_email
                }
                if is_bitcoin:
                    charge_info['source'] = stripe_token
                charge = stripe.Charge.create(**charge_info)
                charge_id = charge.id
            else:
                charge_id = ''
                subscription = customer.subscriptions.create(
                    plan=interval,
                    quantity=int(amount),
                )
                subscription_id = subscription.id

        except stripe.error.CardError as card_error:
            raise DonationError(
                "We're sorry but we had problems charging your card. "
                'Here is what Stripe replied: "%s"' % str(card_error))

        except stripe.error.InvalidRequestError:
            # Invalid parameters were supplied to Stripe's API
            raise DonationError(
                "We're sorry but something went wrong while processing "
                "your card details. No charge was made. Please try "
                "again or get in touch with us.")

        except stripe.error.APIConnectionError:
            # Network communication with Stripe failed
            raise DonationError(
                "We're sorry but we have technical difficulties "
                "reaching our payment processor Stripe. No charge "
                "was done. Please try again later.")

        except stripe.error.AuthenticationError:
            # Authentication with Stripe's API failed
            raise

        except (stripe.StripeError, Exception):
            # The card has been declined, we want to see what happened
            # in Sentry
            raise

        else:
            if not donor:
                profile, created = Profile.objects.get_or_create(user=user)
                donor, created = CTSDonor.objects.get_or_create(
                    profile=profile,
                    email=receipt_email,
                    stripe_customer_id=customer.id,
                )

            # Finally create the donation and return it
            donation = Donation.objects.create(
                interval=interval,
                subscription_amount=amount,
                stripe_customer_id=customer.id,
                stripe_subscription_id=subscription_id,
                receipt_email=receipt_email,
                donor=donor,
            )
            # Only one-time donations are created here. Recurring payments are
            # created by Stripe webhooks.
            if charge_id:
                donation.payment_set.create(
                    amount=amount,
                    stripe_charge_id=charge_id,
                )

            # Send an email message about managing your donation
            message = render_to_string(
                'fundraising/email/thank-you.html',
                {'donation': donation}
            )
            mail_task(
                'Thank you for your donation to CTS',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [donation.receipt_email]
            )

            return donation
