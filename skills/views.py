from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect

from skills.models import Skill, TrainingBit

def skills_overview(request):
    return render(request, 'skills/skills_overview.html', {
        'skills': Skill.objects.all,
    })

def trainingbits_overview(request):
    return render(request, 'skills/trainingbits_overview.html', {
        'trainingbits': TrainingBit.objects.all,
    })

@csrf_protect
def trainingbit_new(request):
    # If something has been uploaded
    errors = ''
    if request.method == 'POST':
        new_trainingbit = TrainingBit(
            author=request.user,
            image=request.FILES['cover-image'],
            name=request.POST['name'],
            description=request.POST['description']
        )
        new_trainingbit.save()
        return HttpResponseRedirect(reverse('trainer_dashboard'))
            # return HttpResponseRedirect('/')
    # By default show training bit form
    return render(request, 'skills/trainingbit_new.html', {
        'trainingbits': TrainingBit.objects.all,
        'form_errors': errors,
    })


def skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    return render(request, 'skills/skill.html', {
        'skill': skill,
    })
