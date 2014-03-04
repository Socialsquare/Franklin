# Inspired by: http://blog.scur.pl/2012/09/highlighting-current-active-page-django/

from django import template
from django.core import urlresolvers


register = template.Library()


@register.simple_tag(takes_context=True)
def current(context, url_name, return_value=' current', **kwargs):
    print(url_name)
    matches = current_url_equals(context, url_name, **kwargs)
    print(matches)
    return return_value if matches else ''


def current_url_equals(context, url_name, **kwargs):
    current_url = False
    try:
        current_url = urlresolvers.resolve(context.get('request').path)
    except:
        pass

    if current_url.url_name == url_name or url_name == current_url.namespace + ':' + current_url.url_name:
        return current_url
    else:
        return False

    # for key in kwargs:
    #     kwarg = kwargs.get(key)
    #     resolved_kwarg = resolved.kwargs.get(key)
    #     if not resolved_kwarg or kwarg != resolved_kwarg:
    #         return False
