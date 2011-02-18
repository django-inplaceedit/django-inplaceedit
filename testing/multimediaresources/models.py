# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

STATUS = (
    ('available', _('Available')),
    ('order', _('Ordered')),
    ('borrow', _('Borrowed')),
    )


class TypeResource(models.Model):
    name = models.CharField(verbose_name=_(u'name'),
                            max_length=100, null=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Type of resource')


class Resource(models.Model):
    name = models.CharField(verbose_name=_(u'Name'),
                            max_length=100, null=False, blank=False)
    created = models.DateField(verbose_name=_(u'Date of created'))
    description = models.TextField(verbose_name=_(u'Description'),
                                   blank=True, null=True)
    status = models.CharField(verbose_name=_(u'Status'),
                              max_length=20, choices=STATUS,
                              default='order', help_text='Status of the resource.',
                              editable=True, null=False, blank=False)
    resource_type = models.ForeignKey(TypeResource, verbose_name=_(u'Type'),
                                     null=False, blank=False, editable=True)
    owner = models.ManyToManyField(User, verbose_name=_(u'Owner'))
    amount = models.IntegerField(verbose_name=_(u'Amount'), null=True, blank=True)
    can_borrow = models.BooleanField(verbose_name=_(u'Can borrow?'))
    available_from = models.DateTimeField(verbose_name=_(u"Will be available from"))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Resources')
