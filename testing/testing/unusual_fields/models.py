import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UnusualModel(models.Model):

    comma_field = models.CommaSeparatedIntegerField(max_length=250)
    decimal_field = models.DecimalField(decimal_places=10, max_digits=20)
    filepath_field = models.FilePathField(path=os.path.join(settings.MEDIA_ROOT, 'images'))
    float_field = models.FloatField()
    generic_ip_field = models.GenericIPAddressField()
    nullboolean_field = models.NullBooleanField()
    big_integer_field = models.BigIntegerField()
    positive_integer_field = models.PositiveIntegerField()
    positive_small_integer_field = models.PositiveSmallIntegerField()
    slug_field = models.SlugField()
    smallinteger_field = models.SmallIntegerField()
    time_field = models.TimeField()
    url_field = models.URLField()
    one_to_one_field = models.OneToOneField(User)

    class Meta:
        verbose_name = _('UnusualModel')
        verbose_name_plural = _('UnusualModels')

    @models.permalink
    def get_absolute_url(self):
        return ('unusual_edit', (self.pk,))

    def __unicode__(self):
        return self.slug_field
