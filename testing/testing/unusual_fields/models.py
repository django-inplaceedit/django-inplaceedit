import os

from django.conf import settings
# Copyright (c) 2010-2013 by Yaco Sistemas <goinnn@gmail.com> or <pmartin@yaco.es>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this programe.  If not, see <http://www.gnu.org/licenses/>.

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
