from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=70,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'***REMOVED***))
    subject = forms.CharField(max_length=100,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'***REMOVED***))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message'***REMOVED***))
    sender = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Your email address'***REMOVED***))
    cc_myself = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['cc_myself'***REMOVED***.label = "CC Myself"
