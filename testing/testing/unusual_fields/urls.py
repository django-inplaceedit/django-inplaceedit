try:
    from django.conf.urls.defaults import patterns, url
except ImportError:  # Django 1.5
    from django.conf.urls import patterns, url


urlpatterns = patterns('testing.unusual_fields.views',
    url(r'^$', 'unusual_index', name='unusual_index'),
    url(r'^(?P<unusual_id>\w+)/$', 'unusual_edit', name="unusual_edit"),
)
