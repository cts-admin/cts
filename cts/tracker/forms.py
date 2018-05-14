from django import forms
from django.core.validators import FileExtensionValidator


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Browse',
                           widget=forms.FileInput(attrs={'class': 'btn btn-default btn-file'}),
                           validators=[FileExtensionValidator(['gpx'])])
