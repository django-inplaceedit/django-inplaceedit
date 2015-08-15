# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UnusualModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comma_field', models.CommaSeparatedIntegerField(max_length=250)),
                ('decimal_field', models.DecimalField(max_digits=20, decimal_places=10)),
                ('filepath_field', models.FilePathField(path=b'/home/pmartin/git-projects/django-inplaceedit/testing/testing/media/images', null=True, blank=True)),
                ('float_field', models.FloatField(null=True, blank=True)),
                ('generic_ip_field', models.CharField(max_length=200)),
                ('nullboolean_field', models.NullBooleanField()),
                ('big_integer_field', models.IntegerField()),
                ('positive_integer_field', models.PositiveIntegerField()),
                ('positive_small_integer_field', models.PositiveSmallIntegerField()),
                ('slug_field', models.SlugField()),
                ('smallinteger_field', models.SmallIntegerField()),
                ('time_field', models.TimeField()),
                ('url_field', models.URLField()),
                ('email_field', models.EmailField(max_length=254)),
                ('one_to_one_field', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'UnusualModel',
                'verbose_name_plural': 'UnusualModels',
            },
        ),
    ]
