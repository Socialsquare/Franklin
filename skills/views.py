from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect

import django.contrib.messages as messages
from permission.decorators import permission_required

from skills.models import Skill, TrainingBit, Project
from skills.forms import ProjectForm

from django_sortable.helpers import sortable_helper

import json


def skills_overview(request, show_hidden=False):

    if request.user.has_perm('skills.show_hidden') and show_hidden:
        skills = Skill.objects.filter(is_public=False)
    else:
        skills = Skill.objects.filter(is_public=True)

    skills = sortable_helper(request, skills)

    return render(request, 'skills/skills_overview.html', {
        'skills': skills,
        'showing_hidden': show_hidden,
    })

def skill_view(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)

    return render(request, 'skills/skill_view.html', {
        'skill': skill,
        'skill_id_get_query': '?skill_id=%u' % skill.id,
    })

def skill_trainingbits_json(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)

    trainingbits = []

    for trainingbit in skill.trainingbits.all():
        d = {
            'id': trainingbit.id,
            'name': trainingbit.name,
            'in_progress': trainingbit.users_in_progress.count(),
            'completed': trainingbit.users_completed.count(),
        }
        trainingbits.append(d)


    return HttpResponse(json.dumps(trainingbits), content_type='application/json')

@csrf_protect
def skill_start(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)

    request.user.skills_in_progress.add(skill)
    messages.success(request, 'You are now taking this skill')

    return HttpResponseRedirect(reverse('skills:skill_view', args=[skill_id]))

@csrf_protect
def skill_stop(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)

    request.user.skills_in_progress.remove(skill)
    messages.info(request, 'You are no longer taking this skill')

    return HttpResponseRedirect(reverse('skills:skill_view', args=[skill_id]))

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

        # Add trainingbits
        items = []
        for key, value in request.POST.items():
            print(key, value)
            if key[0:12] == 'trainingbit-':
                trainingbit_id = int(key[12:])
                items.append(trainingbit_id)
        tbs = TrainingBit.objects.filter(id__in=items)

        # Set the training bits to only the ones chosen on the page
        skill.trainingbits.clear()
        skill.trainingbits.add(*tbs)

        messages.success(request, 'Successfully saved skill')

        # Add tags
        # tags = list(map(lambda s: s.strip('"'), request.POST['tags'].split(' ')))
        # skill.tags.set(*tags)

        # return HttpResponseRedirect(reverse('trainer_dashboard'))
    elif skill_id is not None:
        skill = Skill.objects.get(id__exact=skill_id)
        tags = ' '.join(skill.tags.names())

    # By default show skill form
    # print(list(map(lambda t: t.id, skill.trainingbits.all())))
    try:
        training_bit_ids = list(map(lambda t: t.id, skill.trainingbits.all()))
    except AttributeError:
        training_bit_ids = []

    return render(request, 'skills/skill_edit.html', {
        'skill': skill,
        'trainingbits': TrainingBit.objects.all().extra(order_by=['name']),
        'skill_trainingbit_ids': training_bit_ids,
        'tags': tags,
    })


def trainingbits_overview(request):
    trainingbits = TrainingBit.objects.all()
    trainingbits = sortable_helper(request, trainingbits)
    return render(request, 'skills/trainingbits_overview.html', {
        'trainingbits': trainingbits,
    })

def trainingbit_cover(request, trainingbit_id):
    trainingbit = get_object_or_404(TrainingBit, pk=trainingbit_id)

    try:
        skill_id = request.GET['skill_id']
        request.session['current_skill_id'] = skill_id
    except KeyError:
        pass


    return render(request, 'skills/trainingbit_cover.html', {
        'trainingbit': trainingbit,
        'projects': trainingbit.project_set.all(),
    })

@csrf_protect
def trainingbit_view(request, trainingbit_id):
    trainingbit = get_object_or_404(TrainingBit, pk=trainingbit_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # Save
            project = form.save(commit=False)
            project.author = request.user
            project.trainingbit = trainingbit
            project.save()
            messages.success(request, 'Project was successfully saved')

            request.user.trainingbits_in_progress.remove(trainingbit)
            request.user.trainingbits_completed.add(trainingbit)

            if request.is_ajax():
                d = {
                    'id': project.id,
                    'title': project.title,
                    'content': project.content,
                    'author': project.author.username,
                }
                # The 201 HTTP status code is from my reading of the standard
                # the # correct response to a POST which successfully created a
                # new object.
                # See: http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.2
                return HttpResponse(json.dumps(d), content_type='application/json', status=201)
        else:
            if request.is_ajax():
                return HttpResponse(json.dumps(form.errors), content_type='application/json', status=404)


    try:
        skill_id = request.session['current_skill_id']
        skill = Skill.objects.get(pk=skill_id)
        # get only trainingbits from the current skill
        trainingbits = TrainingBit.objects.filter(skill__id__exact=skill_id)
        print(trainingbits)
    except KeyError:
        # If we're not currently doing any skill just pick some trainingbits
        # we haven't already taken
        trainingbits = TrainingBit.objects.all()

    suggested_trainingbits = trainingbits.exclude(id__in=request.user.trainingbits_completed.all())

    return render(request, 'skills/trainingbit_view.html', {
        'trainingbit': trainingbit,
        'projects': trainingbit.project_set.all(),
        'next': reverse('skills:trainingbit_view', args=[trainingbit_id]),
        'suggested_trainingbits': suggested_trainingbits[:3],
    })

@csrf_protect
def trainingbit_edit(request, trainingbit_id=None):
    trainingbit = None
    tags = ''
    # If something has been uploaded
    if request.method == 'POST':

        if trainingbit_id is None:
            trainingbit = TrainingBit(id=trainingbit_id)
        else:
            trainingbit = get_object_or_404(TrainingBit, pk=trainingbit_id)

        trainingbit.author      = request.user
        trainingbit.name        = request.POST['name']
        trainingbit.description = request.POST['description']
        trainingbit.label       = request.POST['label']

        if 'cover-image' in request.FILES:
        # and request.FILES['cover-image'].size > 0:
            image = request.FILES['cover-image']
        elif trainingbit_id is not None:
            image = TrainingBit.objects.get(id__exact=trainingbit_id).image
        else:
            image = None

        trainingbit.image = image

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
        'labels': TrainingBit.LABELS,
    })

@csrf_protect
def trainingbit_edit_content(request, trainingbit_id):
    trainingbit = get_object_or_404(TrainingBit, pk=trainingbit_id)

    # If a form has been submitted
    if request.method == 'POST':

        print(trainingbit.author)
        print(request.POST['trainingbit_content_json'])
        # Save the training bit
        trainingbit.json_content = request.POST['trainingbit_content_json']
        trainingbit.save()
        messages.success(request, 'Saved training bit')

    # If nothing has been POSTed just show the `edit_content` page
    return render(request, 'skills/trainingbit_edit_content.html', {
        'trainingbit': trainingbit,
    })

@csrf_protect
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

@csrf_protect
def trainingbit_start(request, trainingbit_id):
    trainingbit = get_object_or_404(TrainingBit, pk=trainingbit_id)

    # if trainingbit in request.user.trainingbits_in_progress.all(): # Slow
    if request.user.trainingbits_in_progress.filter(pk=trainingbit.id).exists():
        messages.success(request, 'You are already taking this training bit ;)')

    # elif trainingbit in request.user.trainingbits_completed.all(): # Slow
    elif request.user.trainingbits_completed.filter(pk=trainingbit.id).exists():
        messages.success(request, 'You have already taken this training bit ;)')
    else:
        request.user.trainingbits_in_progress.add(trainingbit)
        messages.success(request, 'You are now taking this training bit')

    return HttpResponseRedirect(reverse('skills:trainingbit_view', args=[trainingbit_id]))

@csrf_protect
def trainingbit_stop(request, trainingbit_id):
    trainingbit = get_object_or_404(TrainingBit, pk=trainingbit_id)

    request.user.trainingbits_in_progress.remove(trainingbit)
    messages.info(request, 'You are no longer taking this training bit')

    return HttpResponseRedirect(reverse('skills:trainingbit_view', args=[trainingbit_id]))


