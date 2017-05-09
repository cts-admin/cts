# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0029_unicode_slugfield_dj19'),
    ***REMOVED***

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(on_delete=models.CASCADE, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ***REMOVED***,
            options={
                'abstract': False,
    ***REMOVED***
            bases=('wagtailcore.page',),
        ),
    ***REMOVED***
