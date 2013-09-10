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
import datetime
import decimal
import json
import transmeta
import sys

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.test import TestCase
from django.test.client import Client


from inplaceeditform.commons import get_adaptor_class

from testing.inplace_transmeta.models import News
from testing.multimediaresources.models import Resource
from testing.unusual_fields.models import UnusualModel

if sys.version_info.major >= 2:
    string = str
else:
    string = basestring


class InplaceTestCase(TestCase):

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

    def __client_login(self):
        client = self.client
        user = 'test'
        password = 'testtest'
        is_login = client.login(username=user, password=password)
        self.assertEqual(is_login, True)
        self.user = User.objects.get(username=user)
        return client

    def _test_get_fields(self, model, field_names=None):
        client = self.__client_login()
        obj = model.objects.all()[0]
        module_name = model._meta.module_name
        app_label = model._meta.app_label
        field_names = field_names or model._meta.get_all_field_names()
        for field in field_names:
            if field == 'id' or field.endswith('_id'):  # id or id fk
                continue
            url = '%s?app_label=%s&module_name=%s&field_name=%s&obj_id=%s' % (reverse('inplace_get_field'),
                                                                              app_label,
                                                                              module_name,
                                                                              field,
                                                                              obj.pk)
            response = client.get(url)
            self.assertEqual(response.status_code, 200)

    def _test_save_fields(self, model, field_names=None):
        client = self.__client_login()
        obj = model.objects.all()[0]
        module_name = model._meta.module_name
        app_label = model._meta.app_label
        field_names = field_names or model._meta.get_all_field_names()
        for field_name in field_names:
            if field_name in transmeta.get_all_translatable_fields(model):
                field = model._meta.get_field_by_name(transmeta.get_fallback_fieldname(field_name))[0]
            else:
                field = model._meta.get_field_by_name(field_name)[0]
            if field_name == 'id' or field_name.endswith('_id'):  # id or id fk
                continue
            if isinstance(field, models.FileField):
                continue
            url = reverse('inplace_save')
            value = getattr(obj, field_name)
            if isinstance(value, datetime.datetime):
                value = '"1982-11-14 03:13:12"'
            elif isinstance(value, datetime.date):
                value = '"1982-11-14"'
            elif isinstance(value, datetime.time):
                value = '"03:13:12"'
            else:
                if hasattr(value, 'all'):
                    value = [str(obj_rel.pk) for obj_rel in value.model.objects.all()]
                elif isinstance(value, decimal.Decimal):
                    value = float(value) + 10
                elif (isinstance(value, string) and
                      isinstance(field, models.CharField) and
                      not isinstance(field, models.CommaSeparatedIntegerField) and
                      not isinstance(field, models.EmailField)):
                    if field.choices:
                        value = field.choices[0][0]
                    else:
                        value += '_save'
                elif isinstance(field, models.CommaSeparatedIntegerField):
                    value += ',44'
                elif isinstance(field, models.EmailField):
                    value = 'xxx@es.com'
                elif isinstance(field, models.ForeignKey):
                    value = field.rel.to.objects.all()[0].pk
                elif isinstance(field, bool):
                    value = not value
                value = json.dumps(value)
            adaptor = get_adaptor_class(obj=obj, field_name=field_name)(None, obj, field_name).name
            data = {'app_label': app_label,
                    'module_name': module_name,
                    'field_name': field_name,
                    'value': value,
                    'obj_id': obj.pk,
                    'adaptor': adaptor}
            response = client.post(url, data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.content.decode('utf-8')).get('errors', None), False)

    def test_get_fields_resource(self):
        self._test_get_fields(Resource)

    def test_save_fields_resource(self):
        self._test_save_fields(Resource)

    def test_get_fields_unusualmodel(self):
        self._test_get_fields(UnusualModel)

    def test_save_fields_unusualmodel(self):
        self._test_save_fields(UnusualModel)

    def test_get_fields_news(self):
        self._test_get_fields(News, field_names=['title', 'description'])

    def test_save_fields_news(self):
        self._test_save_fields(News, field_names=['title', 'description'])
