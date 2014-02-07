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


def trainer_dashboard(request):
    return render(request, 'trainer_dashboard.html', {
        'trainingbits': request.user.trainingbit_set.all(),
        # TrainingBit.objects.l
        # 'shares': None, #Skill.objects.all(),
    })
