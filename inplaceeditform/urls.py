# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('inplaceeditform.views',
    url(r'^save/$', 'save_ajax', name='inplace_save'),
    url(r'^get_field/$', 'get_field', name='inplace_get_field')
)
