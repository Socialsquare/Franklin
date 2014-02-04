from django.http import HttpResponse
from django.shortcuts import render_to_response

from skills.models import Skill


def front_page(request):
    return render_to_response('front_page.html', {
        'name': 'malthe',
        'skills': Skill.objects.all(),
    })


# TODO: this page is a stub
def shares(request):
    return render_to_response('shares.html', {
        'shares': None, #Skill.objects.all(),
    })
