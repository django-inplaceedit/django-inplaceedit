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
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('created', models.DateField(verbose_name='Date of created')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('status', models.CharField(default=b'order', help_text=b'Status of the resource.', max_length=20, verbose_name='Status', choices=[(b'available', 'Available'), (b'order', 'Ordered'), (b'borrow', 'Borrowed')])),
                ('amount', models.IntegerField(null=True, verbose_name='Amount', blank=True)),
                ('can_borrow', models.BooleanField(verbose_name='Can borrow?')),
                ('available_from', models.DateTimeField(verbose_name='Will be available from')),
                ('image', models.ImageField(upload_to=b'images', null=True, verbose_name='Associated Image', blank=True)),
                ('file', models.FileField(upload_to=b'files', null=True, verbose_name='File Text', blank=True)),
                ('owner', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Resources',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TypeResource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
            ],
            options={
                'verbose_name': 'Type of resource',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='resource',
            name='resource_type',
            field=models.ForeignKey(verbose_name='Type', to='multimediaresources.TypeResource'),
            preserve_default=True,
        ),
    ]
