from django.contrib import admin

from .models import Accession, CommonName, Family, Genus, Species, Variety

admin.site.register([Accession, CommonName, Family, Genus, Species, Variety])
