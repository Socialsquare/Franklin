import re

from django import template

from django.contrib.humanize.templatetags.humanize import naturaltime

# For the GCL Flat Page template tag.
from django.conf import settings
from global_change_lab.models import GCLFlatPage

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


# From: http://stackoverflow.com/a/6887723/118608
useserialcomma = True

@register.filter
def listify(values, maxitems=4):
    sercomma = ',' if useserialcomma else ''
    l = len(values)
    if l == 0:
        return ''
    elif l == 1:
        return values[0]
    elif l == 2:
        return values[0] + ' and ' + values[1]
    elif l <= maxitems:
        return ', '.join(values[:l-1]) + sercomma + ' and ' + values[-1]
    else:
        andmoretxt = ' and %d more' % (l - maxitems)
        return ', '.join(values[:maxitems]) + andmoretxt

class GCLFlatpageNode(template.Node):
    def __init__(self, context_name, only_in_footer=False):
        self.context_name = context_name
        self.only_in_footer = only_in_footer

    def render(self, context):
        flatpages = GCLFlatPage.objects.filter(sites__id=settings.SITE_ID)
        if self.only_in_footer:
             flatpages = flatpages.filter(show_in_footer = True)
        context[self.context_name] = flatpages
        return ''

@register.tag
def get_footer_flatpages(parser, token):
    bits = token.split_contents()
    # The very last bit must be the context name
    if bits[-2] != 'as':
        raise template.TemplateSyntaxError(syntax_message)
    context_name = bits[-1]
    return GCLFlatpageNode(context_name, only_in_footer=True)