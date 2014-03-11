import re

from django import template

from django.contrib.humanize.templatetags.humanize import naturaltime

register = template.Library()

re_timesince = re.compile(r'(.+),.* ago')

# From django/contrib/humanize/templatetags/humanize.py (the `naturaltime` filter)
@register.filter
def pretty_timesince(value):
    """
    Returns a string which shows how many seconds, minutes, hours or days ago
    the supplied date and time value was, compared to the current timestamp

    Takes the `naturaltime` from the django.contrib.humanize templatetags and
    removes `, XX YY` from `UU VV, XX YY hours ago`. So that it only shows
    X weeks
    X days
    X hours
    X minutes
    X seconds
    and not a mix of two time units.
    e.g. it turns `4 weeks, 3 days ago` into `4 weeks ago`.
    """

    t_str = naturaltime(value)
    match = re_timesince.match(t_str)

    if match:
        return match.group(1) + ' ago'
    else:
        return t_str
