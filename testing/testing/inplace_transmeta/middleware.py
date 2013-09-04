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
                request.session['django_language'] = forced_lang
