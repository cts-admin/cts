from django.contrib import admin

from .models import CommonName, Family, Genus, Species, Variety

admin.site.register([CommonName, Family, Genus, Species, Variety])
