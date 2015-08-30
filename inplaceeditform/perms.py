# -*- coding: utf-8 -*-
# Copyright (c) 2010-2013 by Yaco Sistemas <goinnn@gmail.com>
#               2015 by Pablo Martín <goinnn@gmail.com>
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

from inplaceeditform.commons import get_module_name


class SuperUserPermEditInline(object):

    @classmethod
    def can_edit(cls, field):
        return field.request.user.is_authenticated and field.request.user.is_superuser


class AdminDjangoPermEditInline(SuperUserPermEditInline):

    @classmethod
    def can_edit(cls, field):
        is_super_user = super(AdminDjangoPermEditInline, cls).can_edit(field)
        if not is_super_user:
            model = field.model
            model_edit = '%s.change_%s' % (model._meta.app_label,
                                           get_module_name(model))
            return field.request.user.has_perm(model_edit)
        return is_super_user
