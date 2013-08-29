try:
    from django.conf.urls.defaults import patterns, url
except ImportError:  # Django 1.5
    from django.conf.urls import patterns, url


urlpatterns = patterns('testing.multimediaresources.views',
    url(r'^$', 'multimediaresources_index', name='multimediaresources_index'),
    url(r'^(?P<resource_id>\w+)/$', 'multimediaresources_edit', name="multimediaresources_edit"),
)
