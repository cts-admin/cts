from django.db import migrations


def convert_site_country_to_model(apps, schema_editor):
    Site = apps.get_model('plant_database', 'Site')
    Country = apps.get_model('plant_database', 'Country')
    for site in Site.objects.all():
        country, _ = Country.objects.get_or_create(name=site.country)
        site.country_id = country


class Migration(migrations.Migration):

    dependencies = [
        ('plant_database', '0004_auto_20200628_0137'),
    ]

    operations = [
        migrations.RunPython(convert_site_country_to_model)
    ]
