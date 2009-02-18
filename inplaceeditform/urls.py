# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns

urlpatterns = patterns('inplaceeditform.views',
    # Save
    (r'^$', 'save_ajax'),
)
