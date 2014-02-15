from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect

import django.contrib.messages as messages
from permission.decorators import permission_required

from skills.models import Skill, TrainingBit


def skills_overview(request, show_hidden=False):

    if request.user.has_perm('skills.show_hidden') and show_hidden:
        skills = Skill.objects.filter(is_public=False)
    else:
        skills = Skill.objects.filter(is_public=True)


    return render(request, 'skills/skills_overview.html', {
        'skills': skills,
        'showing_hidden': show_hidden,
    })

def skill_view(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    return render(request, 'skills/skill_view.html', {
        'skill': skill,
    })

@csrf_protect
#@permission_required('skill.publicize')
def skill_publicize(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    if request.user.has_perm('skill.publicize', skill):
        if skill.is_public:
            skill.is_public = False
            messages.info(request, 'The skill is no longer public')
        else:
            skill.is_public = True
            messages.success(request, 'The skill is now public')
        skill.save()
        return HttpResponseRedirect(reverse('skills:skill_view', args=[skill_id]))
    else:
        messages.error(request, 'You do not have permission to make this skill public')
        return HttpResponseRedirect(reverse('skills:skill_view', args=[skill_id]))

def skill_delete(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    if  request.user.has_perm('skill.delete', skill):
        skill.delete()
        messages.success(request, 'The skill was deleted')
        return HttpResponseRedirect(reverse('skills:skills_overview'))
    else:
        messages.error(request, 'You do not have permission to delete this skill')
        return HttpResponseRedirect(reverse('skills:skill_view', skill_id))

@csrf_protect
def skill_edit(request, skill_id=None):
    skill = None
    tags = ''
    # If something has been uploaded
    if request.method == 'POST':

        if 'skill-icon' in request.FILES:
        # and request.FILES['cover-image'].size > 0:
            image = request.FILES['skill-icon']
        elif skill_id is not None:
            image = Skill.objects.get(id__exact=skill_id).image
        else:
            image = None

        if image is not None:
            img_d = {'image': image}
        else:
            img_d = {}

        skill = Skill(
            id=skill_id,
            author=request.user,
            name=request.POST['name'],
            description=request.POST['description'],
            **img_d
        )
        skill.save()

        tags = list(map(lambda s: s.strip('"'), request.POST['tags'].split(' ')))
        skill.tags.set(*tags)

        return HttpResponseRedirect(reverse('trainer_dashboard'))
    elif skill_id is not None:
        skill = Skill.objects.get(id__exact=skill_id)
        tags = ' '.join(skill.tags.names())

    # By default show skill form
    return render(request, 'skills/skill_edit.html', {
        'skill': skill,
        'tags': tags,
    })


def trainingbits_overview(request):
    return render(request, 'skills/trainingbits_overview.html', {
        'trainingbits': TrainingBit.objects.all,
    })


def trainingbit_view(request, trainingbit_id):
    return render(request, 'skills/trainingbit_view.html', {
        'trainingbit': TrainingBit.objects.get(id__exact=trainingbit_id),
        'next': reverse('skills:trainingbit_view', args=[trainingbit_id]),
    })

@csrf_protect
def trainingbit_edit(request, trainingbit_id=None):
    trainingbit = None
    tags = ''
    # If something has been uploaded
    if request.method == 'POST':

        if 'cover-image' in request.FILES:
        # and request.FILES['cover-image'].size > 0:
            image = request.FILES['cover-image']
        elif trainingbit_id is not None:
            image = TrainingBit.objects.get(id__exact=trainingbit_id).image
        else:
            image = None

        if image is not None:
            img_d = {'image': image}
        else:
            img_d = {}

        trainingbit = TrainingBit(
            id=trainingbit_id,
            author=request.user,
            name=request.POST['name'],
            description=request.POST['description'],
            **img_d
        )
        trainingbit.save()
        trainingbit_id = trainingbit.id

        tags = list(map(lambda s: s.strip('"'), request.POST['tags'].split(' ')))
        trainingbit.tags.set(*tags)

        # return HttpResponseRedirect(reverse('trainer_dashboard'))
        return HttpResponseRedirect(reverse('skills:trainingbit_edit_content', args=[trainingbit_id]))
            # return HttpResponseRedirect('/')
    elif trainingbit_id is not None:
        trainingbit = TrainingBit.objects.get(id__exact=trainingbit_id)
        tags = ' '.join(trainingbit.tags.names())

    # By default show training bit form
    return render(request, 'skills/trainingbit_edit.html', {
        'trainingbit': trainingbit,
        'tags': tags,
    })

# TODO: this is a stub, that should be implemented
@csrf_protect
def trainingbit_edit_content(request, trainingbit_id=None):
    return render(request, 'skills/trainingbit_edit_content.html', {
        'trainingbit': TrainingBit.objects.get(id__exact=trainingbit_id),
    })

def trainingbit_delete(request, trainingbit_id):
    trainingbit = TrainingBit.objects.filter(id__exact=trainingbit_id)
    if request.user.has_perm('trainingbit.delete', trainingbit):
        trainingbit.delete()
        return HttpResponseRedirect(reverse('skills:trainingbits_overview'))
    else:
        return HttpResponseRedirect(reverse('skills:trainingbit_view', trainingbit_id))

# Using the django-permissions functions like this:
# @permission_required('trainingbit.recommend')
# def trainingbit_recommend(request, *args, **kwargs):
#     trainingbit_id = kwargs['trainingbit_id']
#
# You have to name your capture groups in urls.py otherwise it will not work

@csrf_protect
def trainingbit_recommend(request, trainingbit_id):
    trainingbit = get_object_or_404(TrainingBit, pk=trainingbit_id)
    if request.user.has_perm('trainingbit.recommend', trainingbit):
        if trainingbit.recommended:
            trainingbit.recommended = False
            messages.info(request, 'The training bit is no longer recommended')
        else:
            trainingbit.recommended = True
            messages.success(request, 'Successfully recommended training bit')
        trainingbit.save()
        return HttpResponseRedirect(reverse('skills:trainingbit_view', args=[trainingbit_id]))
    else:
        messages.error(request, 'You do not have permission to recommend this training bit')
        return HttpResponseRedirect(reverse('skills:trainingbit_view', args=[trainingbit_id]))



