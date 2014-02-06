from django.http import HttpResponse
from django.shortcuts import render

from skills.models import Skill


def front_page(request):
    return render(request, 'front_page.html', {
        'name': 'malthe',
        'skills': Skill.objects.all(),
    })


# TODO: this page is a stub
def shares(request):
    return render(request, 'shares.html', {
        'shares': None, #Skill.objects.all(),
    })
