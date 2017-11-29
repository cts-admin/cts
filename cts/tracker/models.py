from django.contrib.gis.db import models


class ProvisionalSeedZone(models.Model):
    objectid = models.BigIntegerField()
    fid_level_field = models.BigIntegerField()
    area = models.FloatField()
    perimeter = models.FloatField()
    eco = models.CharField(max_length=7)
    level3 = models.IntegerField()
    level3_nam = models.CharField(max_length=90)
    fid_2017_n = models.BigIntegerField()
    tmin_class = models.CharField(max_length=50)
    ahm_class = models.CharField(max_length=50)
    seed_zone = models.CharField(max_length=50)
    new_label = models.CharField(max_length=30)
    ahm_name = models.CharField(max_length=40)
    geom = models.MultiPolygonField(srid=3857)


class Waypoint(models.Model):
    name = models.CharField(max_length=32)
    geometry = models.PointField(srid=3857)
    objects = models.GeoManager()

    def __unicode__(self):
        return '{} {} {}'.format(self.name, self.geometry.x, self.geometry.y)


class WorldBorder(models.Model):
    # The following are all regular Django fields
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific
    mpoly = models.MultiPolygonField()

    def __str__(self):
        return self.name
