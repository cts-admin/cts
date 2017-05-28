from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=70, help_text="Your name")
    subject = forms.CharField(max_length=100)
    message = forms.Textarea()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
