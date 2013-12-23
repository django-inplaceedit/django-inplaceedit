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

from django.conf import settings
try:
    from django.conf.urls import include, patterns, url
except ImportError:  # Django < 1.4
    from django.conf.urls.defaults import include, patterns, url

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext

admin.autodiscover()

js_info_dict = {
    'packages': ('django.conf',),
}

urlpatterns = patterns('',
    url(r'^inplaceeditform/', include('inplaceeditform.urls')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^multimediaresources/', include('testing.multimediaresources.urls')),
    url(r'^unusualfields/', include('testing.unusual_fields.urls')),
)


def index(request):
    context = {}
    context['multimediaresources_url'] = reverse('multimediaresources_index')
    context['unusual_url'] = reverse('unusual_index')
    if 'testing.inplace_transmeta' in settings.INSTALLED_APPS:
        context['news_url'] = reverse('news_index')
    if 'testing.example_extra_fields' in settings.INSTALLED_APPS:
        context['extra_url'] = reverse('extra_index')
    return render_to_response('index.html',
                              context,
                              context_instance=RequestContext(request))

urlpatterns += patterns('',
    url(r'^$', index))

if 'testing.inplace_transmeta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^news/', include('testing.inplace_transmeta.urls')),
    )

if 'testing.example_extra_fields' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^extra_fields/', include('testing.example_extra_fields.urls'))
    )
    if 'ajax_select' in settings.INSTALLED_APPS:
        from ajax_select import urls as ajax_select_urls
        urlpatterns += patterns('',
            url(r'^ajax_select/', include(ajax_select_urls))
        )

urlpatterns += patterns('',
    (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
     'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT,
      'show_indexes': True}),
)
