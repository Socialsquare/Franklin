from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from skills.models import Skill, TrainingBit

def skills_overview(request):
    return render(request, 'skills/skills_overview.html', {
        'skills': Skill.objects.all,
    })

def trainingbits_overview(request):
    return render(request, 'skills/trainingbits_overview.html', {
        'trainingbits': TrainingBit.objects.all,
    })

def skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    return render(request, 'skills/skill.html', {
        'skill': skill,
    })
