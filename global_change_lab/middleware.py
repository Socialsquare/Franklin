
# From: https://gist.github.com/vstoykov/1366794

class ForceDefaultLanguageMiddleware(object):
    """
    Ignore Accept-Language HTTP headers
    This will force the I18N machinery to always choose settings.LANGUAGE_CODE
    as the default initial language, unless another one is set via sessions or cookies
    Should be installed *before* any middleware that checks request.META['HTTP_ACCEPT_LANGUAGE'],
    namely django.middleware.locale.LocaleMiddleware
    """
    def process_request(self, request):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            del request.META['HTTP_ACCEPT_LANGUAGE']


from django.http import HttpResponseRedirect
import re

# Redirect
# http://globalchangelab.cloudcontrolled.com -> http://www.globalchangelab.org
class CloudControlRedirectMiddleware(object):
    def process_request(self, request):
        if request.META['HTTP_HOST'].startswith('globalchangelab.cloudcontrolled.com'):
            url = request.get_full_path()
            return HttpResponseRedirect('http://www.globalchangelab.org' + url)
