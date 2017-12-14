from django import forms
from django.conf import settings

from .models import CorporateMember
from home.tasks import mail_task


class CorporateMemberSignUpForm(forms.ModelForm):
    amount = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control'}
        ),
        label='Donation amount',
        help_text='Enter an integer in US$ without the dollar sign.',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checkbox_fields = []
        self.radio_select_fields = []
        self.label_fields = []
        self.fields['logo'].required = True
        self.fields['cts_usage'].required = True
        for name, field in self.fields.items():
            help_text = field.help_text
            if help_text:
                help_text = ' (' + help_text + ')'
                self.fields[name].help_text = ''
            self.fields[name].widget.attrs = {'placeholder': field.label + help_text}

            if isinstance(field.widget, forms.CheckboxInput):
                self.checkbox_fields.append(name)
            elif isinstance(field.widget, forms.RadioSelect):
                self.radio_select_fields.append(name)
            elif isinstance(field.widget, (forms.FileInput, forms.Select)):
                self.label_fields.append(name)

        self.fields['billing_name'].widget.attrs['class'] = 'form-control'
        self.fields['billing_name'].widget.attrs['placeholder'] = (
            "Billing name (If different from above name)."
        )
        self.fields['billing_name'].help_text = (
            "For example, this might be your full registered company name."
        )
        self.fields['url'].widget.attrs['class'] = 'form-control'
        self.fields['contact_name'].widget.attrs['class'] = 'form-control'
        self.fields['contact_email'].widget.attrs['class'] = 'form-control'
        self.fields['billing_email'].widget.attrs['class'] = 'form-control'
        self.fields['display_name'].widget.attrs['class'] = 'form-control'
        self.fields['display_name'].widget.attrs['placeholder'] = (
            "Your organization's name as you'd like it to appear on our website."
        )
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['address'].widget.attrs['placeholder'] = (
            'Mailing address'
        )
        self.fields['address'].help_text = (
            'We can send the invoice by email, but we need a contact address.'
        )
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['placeholder'] = (
            "A short paragraph that describes your organization and its "
            "activities, written as if CTS were describing your company "
            "to a third party."
        )
        self.fields['description'].help_text = (
            """We'll use this text on the <a href="/members/corporate-members/">
            corporate membership page</a>; you can use the existing descriptions
            as a guide for flavor we're looking for."""
        )
        self.fields['cts_usage'].widget.attrs['class'] = 'form-control'
        self.fields['cts_usage'].widget.attrs['placeholder'] = (
            'Does your organization plan to use any services offered by CTS?'
        )
        self.fields['cts_usage'].label = 'CTS Usage'
        self.fields['cts_usage'].help_text = (
            "This won't be displayed publicly but helps the CTS Board "
            "to evaluate your application."
        )
        self.fields['amount'].widget.attrs['class'] = 'form-control'
        self.fields['amount'].help_text = (
            """Enter an amount above and the appropriate membership level will
            be automatically selected. Or select a membership level below and
            the minimum donation will be entered for you. See
            <a href="/members/corporate-membership/#dues">dues</a> for
            details on the levels."""
        )
        self.fields['membership_level'].widget.attrs['class'] = 'form-control'

    class Meta:
        fields = [
            'display_name',
            'billing_name',
            'logo',
            'url',
            'contact_name',
            'contact_email',
            'billing_email',
            'address',
            'description',
            'cts_usage',
            'amount',
            'membership_level',
        ]
        model = CorporateMember

    @property
    def is_renewing(self):
        return not self.instance._state.adding

    def save(self, *args, **kwargs):
        is_renewing = self.is_renewing  # self.is_renewing changes after super()
        instance = super().save(*args, **kwargs)
        mail_task(
            'CTS Corporate Membership %s: %s' % (
                'Renewal' if is_renewing else 'Application',
                self.instance.display_name,
            ),
            "Thank you for %s a corporate member of Conservation Technology Solutions Inc! %s" % (
                'renewing as' if is_renewing else 'applying to be',
                "Your renewal has been received, and we'll follow up with an invoice soon." if is_renewing else
                "Your application is being reviewed, and we'll follow up a "
                "response from the board as soon as possible.",
            ),
            settings.DEFAULT_FROM_EMAIL,
            [
                settings.DEFAULT_FROM_EMAIL,
                self.instance.contact_email,
                'ctsadmin@conservationtechnologysolutions.com',
            ],
        )
        instance.invoice_set.create(amount=self.cleaned_data['amount'])
        return instance
