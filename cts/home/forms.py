from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=70,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    subject = forms.CharField(max_length=100,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message'}))
    sender = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Your email address'}))
    cc_myself = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['cc_myself'].label = "CC Myself"
