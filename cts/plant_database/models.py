from datetime import date

from django.contrib.auth.models import User
from django.contrib.gis.db import models


class Collector(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return ' '.join([self.first_name, self.last_name])


class CommonName(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Common name"
        verbose_name_plural = "Common names"


class Family(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Families"


class Genus(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Genera"


class Species(models.Model):
    genus = models.ForeignKey(Genus, on_delete=models.CASCADE)
    common_name = models.ManyToManyField(CommonName)
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Species"


class Variety(models.Model):
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Varieties"


class Country(models.Model):
    name = models.CharField(max_length=70, blank=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"


class Site(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    major_country_area = models.CharField(max_length=70, blank=True)  # e.g. a U.S. state
    minor_country_area = models.CharField(max_length=70, blank=True)  # e.g. a U.S. county
    locality = models.CharField(max_length=70, blank=True)  # e.g. local name like 'Saltflat Springs'

    def __str__(self):
        return ', '.join([self.country, self.major_country_area, self.minor_country_area, self.locality])


class Accession(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True)
    genus = models.ForeignKey(Genus, on_delete=models.SET_NULL, null=True)
    species = models.ForeignKey(Species, on_delete=models.SET_NULL, null=True)
    variety = models.ForeignKey(Variety, on_delete=models.SET_NULL, null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)
    collectors = models.ManyToManyField(Collector)
    plant_total = models.IntegerField()
    # TODO - Don't allow sample size to be greater than plant total
    sample_size = models.IntegerField()
    percent_flowering = models.FloatField(max_length=6)
    percent_fruiting = models.FloatField(max_length=6)
    storage_location = models.CharField(max_length=200)
    location = models.PointField()  # GPS location it was collected from
    altitude = models.FloatField(max_length=6)
    bank_date = models.DateField(default=date.today)  # When accession was added to the seed bank

    def __str__(self):
        if self.variety is not None:
            return ' '.join([self.genus.name, self.species.name, 'var.', self.variety.name])
        else:
            return ' '.join([self.genus.name, self.species.name])


# TODO
"""
Refactor Accessions so some properties become those of a SeedAccession in anticipation of
LivingAccessions.
"""


class SeedAccession(Accession):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
