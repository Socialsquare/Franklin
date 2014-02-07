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


def trainingbit_view(request, trainingbit_id):
    return render(request, 'skills/trainingbit_view.html', {
        'trainingbit': TrainingBit.objects.get(id__exact=trainingbit_id),
    })

@csrf_protect
def trainingbit_edit(request, trainingbit_id=None):
    trainingbit = None
    # If something has been uploaded
    if request.method == 'POST':

        if 'cover-image' in request.FILES:
        # and request.FILES['cover-image'].size > 0:
            image = request.FILES['cover-image']
        else:
            image = TrainingBit.objects.get(id__exact=trainingbit_id).image

        trainingbit = TrainingBit(
            id=trainingbit_id,
            author=request.user,
            name=request.POST['name'],
            description=request.POST['description'],
            image=image
        )
        trainingbit.save()
        return HttpResponseRedirect(reverse('trainer_dashboard'))
            # return HttpResponseRedirect('/')
    elif trainingbit_id is not None:
        trainingbit = TrainingBit.objects.get(id__exact=trainingbit_id)

    # By default show training bit form
    return render(request, 'skills/trainingbit_edit.html', {
        'trainingbit': trainingbit,
    })

# TODO: this is a stub, that should be implemented
@csrf_protect
def trainingbit_edit_content(request, trainingbit_id=None):
    return HttpResponseRedirect('/')

def trainingbit_delete(request, trainingbit_id):
    trainingbit = TrainingBit.objects.filter(id__exact=trainingbit_id)
    if trainingbit.get().author == request.user or request.user.is_admin():
        trainingbit.delete()
        return HttpResponseRedirect(reverse('skills:trainingbits_overview'))
    else:
        return HttpResponseRedirect(reverse('skills:trainingbit_view', trainingbit_id))



def skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    return render(request, 'skills/skill.html', {
        'skill': skill,
    })
