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
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

STATUS = (
    ('available', _('Available')),
    ('order', _('Ordered')),
    ('borrow', _('Borrowed')),
)


@python_2_unicode_compatible
class TypeResource(models.Model):
    name = models.CharField(verbose_name=_(u'name'),
                            max_length=100, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Type of resource')


@python_2_unicode_compatible
class Resource(models.Model):
    name = models.CharField(verbose_name=_(u'Name'),
                            max_length=100, null=False, blank=False,
                            unique=True)
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
    image = models.ImageField(verbose_name=_(u"Associated Image"), null=True, blank=True, upload_to="images")
    file = models.FileField(verbose_name=_(u"File Text"), null=True, blank=True, upload_to="files")

    class Meta:
        verbose_name = _(u'Resources')

    @models.permalink
    def get_absolute_url(self):
        return ('multimediaresources_edit', (self.pk,))

    def __str__(self):
        return self.name
