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

import transmeta

from django.db import models
from django.utils.translation import ugettext_lazy as _


class News(models.Model, metaclass=transmeta.TransMeta):

    title = models.CharField(verbose_name=_(u'Title'),
                             max_length=100)
    description = models.TextField(verbose_name=_(u'Description'),
                                   blank=True, null=True)

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('Newss')
        translate = ('description', 'title', )

    @models.permalink
    def get_absolute_url(self):
        return ('news_edit', (self.pk,))

    def __unicode__(self):
        return self.title
