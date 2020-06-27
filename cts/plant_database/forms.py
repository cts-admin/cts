from datetime import date

from django import forms

from .models import Accession, Family, Genus


def get_last_accession_number():
    try:
        latest = Accession.objects.latest('id')
        return latest.id + 1
    except Accession.DoesNotExist:
        return 1


class AccessionForm(forms.Form):
    """
    Dynamic fields for Collectors taken from: Yuji 'Tomita' Tomita - https://stackoverflow.com/a/6142749/1175701
    """
    accession_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                          disabled=True)

    col_fname = forms.CharField(max_length=30, label="Collector's first name",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    col_lname = forms.CharField(max_length=30, label="Collector's last name",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))
    # Include a hidden field to track number of additional collectors
    add_collector_count = forms.CharField(widget=forms.HiddenInput())

    common_name = forms.CharField(max_length=70, label="Species common name",
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Common name'}))

    family = forms.ModelChoiceField(queryset=Family.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    genus = forms.ModelChoiceField(queryset=Genus.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    species = forms.CharField(max_length=70, label="Species scientific name",
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Species name'}))

    variety = forms.CharField(max_length=70, label="Variety",
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Variety name'}),
                              required=False)

    country = forms.CharField(max_length=70, label="Country",
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
                              required=False)
    maj_country = forms.CharField(max_length=70, label="Major country area",
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control', 'placeholder': 'e.g. a U.S. state'}),
                                  required=False)
    min_country = forms.CharField(max_length=70, label="Minor country area",
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control', 'placeholder': 'e.g. a U.S. county'}),
                                  required=False)
    locality = forms.CharField(max_length=70, label="Locality",
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'e.g. local name like "Saltflat Springs"'}), required=False)

    plant_total = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                     'placeholder':
                                                                         'Total number of target plants at site'}))
    sample_size = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                     'placeholder':
                                                                         'Total number of plants sampled from'}))
    percent_flowering = forms.FloatField(min_value=0, max_value=100,
                                         widget=forms.NumberInput(attrs={'class': 'form-control'}))
    percent_fruiting = forms.FloatField(min_value=0, max_value=100,
                                        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    storage_location = forms.CharField(max_length=200, label="Storage location",
                                       widget=forms.TextInput(
                                           attrs={'class': 'form-control', 'placeholder': 'Storage location'}))
    # TODO add dropdown to choose coordinate system
    latitude = forms.FloatField(min_value=-90, max_value=90, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    longitude = forms.FloatField(min_value=-180, max_value=180,
                                 widget=forms.NumberInput(attrs={'class': 'form-control'}))
    # TODO add dropdown to choose unit for elevation
    altitude = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    bank_date = forms.DateField(initial=date.today)  # When accession was added to the seed bank

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 1)

        super(AccessionForm, self).__init__(*args, **kwargs)
        self.fields['add_collector_count'].initial = extra_fields
        self.fields['accession_number'].initial = get_last_accession_number()

        for index in range(1, int(extra_fields)):
            self.fields['add_collector_{index}'.format(index=index)] = forms.CharField()
