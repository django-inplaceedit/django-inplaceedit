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

from django.utils import translation


class LocaleMiddleware(object):
    """This middleware checks if we come from a Plone site
    that set a language cookie. In that case we use that
    language"""

    def process_request(self, request):
        forced_lang = request.GET.get('set_language', None)
        request.forced_lang = forced_lang
        if forced_lang:
            translation.activate(forced_lang)
            request.LANGUAGE_CODE = translation.get_language()
            if hasattr(request, 'session'):
                key_name = getattr(translation, 'LANGUAGE_SESSION_KEY',
                                   'django_language')
                request.session[key_name] = forced_lang
