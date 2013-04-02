"""
Dummy models to reproduce the generic FK error in the django inplace edit project.
"""

# django imports
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _


class Address(models.Model):
    """
    Generic object to set a postal address.
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    address = models.CharField(
        max_length=200, default="", blank=True,
        verbose_name=_("Address"))

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __unicode__(self):
        return '%s, %s' % (self.address)

class Document(models.Model):
    """
    Class to centralize the management of documents.
    """
    name = models.CharField(_('Name'), max_length=200, unique=True)

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")

    def __unicode__(self):
        return '%s' % (self.name)

class Company(models.Model):
    """
    Database model to store the companies information.
    """
    name = models.CharField(_('Name'), max_length=200, unique=True)
    logo = models.ForeignKey(Document, null=True, blank=True, verbose_name=_("logo"))
    addresses = generic.GenericRelation(
        Address, verbose_name=_('Addresses'))

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __unicode__(self):
        return '%s' % (self.name)
