# -*- coding: utf-8 -*-
import os

from django.core import serializers
from django.db import migrations


fixture_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../fixtures'))
fixture_filename = 'initial_data.json'


def load_fixture(apps, schema_editor):
    fixture_file = os.path.join(fixture_dir, fixture_filename)

    fixture = open(fixture_file, 'rb')
    objects = serializers.deserialize('json', fixture, ignorenonexistent=True)
    for obj in objects:
        obj.save()
    fixture.close()


def unload_fixture(apps, schema_editor):
    "Brutally deleting all entries for this model..."

    UnusualModel = apps.get_model("unusual_fields", "UnusualModel")
    UnusualModel.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('unusual_fields', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture, reverse_code=unload_fixture),
    ]
