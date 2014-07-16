# Inspired by: http://blog.scur.pl/2012/09/highlighting-current-active-page-django/

from django import template
from django.core import urlresolvers


register = template.Library()


@register.simple_tag(takes_context=True)
def current(context, url_name, return_value=' current', **kwargs):
    matches = current_url_equals(context, url_name, **kwargs)
    return return_value if matches else ''


@register.simple_tag(takes_context=True)
def current_url_name(context, **kwargs):
    try:
        url_name = urlresolvers.resolve(context.get('request').path).url_name
        return url_name
    except:
        return ""



def current_url_equals(context, url_name, **kwargs):
    current_url = False
    try:
        current_url = urlresolvers.resolve(context.get('request').path)
        if current_url.url_name == url_name or url_name == current_url.namespace + ':' + current_url.url_name:
            return current_url
    except:
        pass
    return False

    # for key in kwargs:
    #     kwarg = kwargs.get(key)
    #     resolved_kwarg = resolved.kwargs.get(key)
    #     if not resolved_kwarg or kwarg != resolved_kwarg:
    #         return False
