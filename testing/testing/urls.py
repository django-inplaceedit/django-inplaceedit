# -*- coding: utf-8 -*-

from django.conf import settings
try:
    from django.conf.urls.defaults import include, patterns, url
except ImportError:  # Django 1.5
    from django.conf.urls import include, patterns, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
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

from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):
    return render_to_response('index.html',
                              context_instance=RequestContext(request))

urlpatterns += patterns('',
    url(r'^$', index))

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$',
     'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
)
