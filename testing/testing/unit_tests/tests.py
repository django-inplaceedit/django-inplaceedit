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

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from testing.multimediaresources.models import Resource
from testing.unusual_fields.models import UnusualModel


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

    def _test_get_fields(self, model):
        client = self.__client_login()
        obj = model.objects.all()[0]
        module_name = model._meta.module_name
        app_label = model._meta.app_label
        field_names = model._meta.get_all_field_names() + [m2m.name for m2m in model._meta.many_to_many]
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

    def test_get_fields_resource(self):
        self._test_get_fields(Resource)

    def test_get_fields_unusualmodel(self):
        self._test_get_fields(UnusualModel)
