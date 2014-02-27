from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect

import django.contrib.messages as messages
from permission.decorators import permission_required

from skills.models import Skill, TrainingBit, Project, Topic
from skills.forms import ProjectForm, TopicForm

from django_sortable.helpers import sortable_helper

import json


def skills_overview(request, topic_name=None, show_hidden=False):
    # Show from topic
    if topic_name is not None:
        topic = get_object_or_404(Topic, name=topic_name)
        skills = topic.skills.all()
    else:
        topic = None
        skills = Skill.objects.all()

    # Show public/hidden
    if request.user.has_perm('skills.show_hidden') and show_hidden:
        skills = skills.filter(is_public=False)
    else:
        skills = skills.filter(is_public=True)

    # Sort
    skills = sortable_helper(request, skills)

    return render(request, 'skills/skills_overview.html', {
        'skills': skills,
        'showing_hidden': show_hidden,
        'topics': Topic.objects.all(),
        'topic_chosen': topic,
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



        # Add trainingbits (ORDER IS IMPORTANT HERE)
        selected_trainingbit_pos_pk = request.POST.getlist('trainingbit-pos-pk[]')
        pos_pk = [v.split(',') for v in selected_trainingbit_pos_pk]
        pos = [int(p[0].strip()) for p in pos_pk]
        pks = [int(p[1].strip()) for p in pos_pk]
        tb_dict = TrainingBit.objects.in_bulk(pks)

        # - Sort trainingbit primary keys by position
        sorted_pos_pk_list = sorted(zip(pos,pks))

        # - Make an ordered list of trainingbits
        tbs = []
        for pos, pk in sorted_pos_pk_list:
            tbs.append(tb_dict[pk])

        # - Set the training bits to only the ones chosen on the page
        skill.trainingbits.clear()
        skill.trainingbits.add(*tbs)

        # Add topics
        selected_topic_pks = request.POST.getlist('topic-pks[]')
        selected_topic_pks = [int(s) for s in selected_topic_pks]
        print(selected_topic_pks)
        topics = Topic.objects.filter(pk__in=selected_topic_pks)
        print(topics)
        skill.topic_set.clear()
        skill.topic_set.add(*topics)

        messages.success(request, 'Successfully saved skill')

    elif skill_id is not None:
        skill = Skill.objects.get(id__exact=skill_id)
        selected_topic_pks = [t.pk for t in skill.topic_set.all()]
    else:
        skill = None
        selected_topic_pks = []

    if skill is None:
        trainingbits_chosen    = []
        trainingbits_available = TrainingBit.objects.all()
    else:
        trainingbits_chosen    = skill.trainingbits.all() #.extra(order_by=['sort_value'])
        trainingbits_available = TrainingBit.objects.exclude(id__in=trainingbits_chosen.values('id')).extra(order_by=['name'])

    try:
        training_bit_ids = list(map(lambda t: t.id, skill.trainingbits.all()))
    except AttributeError:
        training_bit_ids = []

    # suggested_trainingbits = trainingbits.exclude(id__in=request.user.trainingbits_completed.all())

    return render(request, 'skills/skill_edit.html', {
        'skill': skill,
        'trainingbits_chosen': trainingbits_chosen,
        'trainingbits_available': trainingbits_available,
        'topics': Topic.objects.all(),
        'selected_topic_pks': selected_topic_pks,
    })


def trainingbits_overview(request, topic_name=None):
    if topic_name is not None:
        topic = get_object_or_404(Topic, name=topic_name)
        trainingbits = topic.trainingbits.all()
    else:
        topic = None
        trainingbits = TrainingBit.objects.all()

    trainingbits = sortable_helper(request, trainingbits)
    return render(request, 'skills/trainingbits_overview.html', {
        'trainingbits': trainingbits,
        'topics': Topic.objects.all(),
        'topic_chosen': topic,
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

def get_suggested_trainingbits(user, session):
    # documentation on `values_list`: https://docs.djangoproject.com/en/1.6/ref/models/querysets/#values-list

    # If we're currently in a skill use that for suggestions, otherwise just
    # give any suggestion
    try:
        skill_id = session['current_skill_id']
        skill = Skill.objects.get(pk=skill_id)
        # get only trainingbits from the current skill
        trainingbits = skill.trainingbits #TrainingBit.objects.filter(skill__id__exact=skill_id)
    except KeyError:
        # If we're not currently doing any skill just pick some trainingbits
        # we haven't already taken
        trainingbits = TrainingBit.objects.all()

    # Don't suggest training bits the user has already completed, including the
    # one he is about to complete. (Because when we show the suggestions he
    # will have completed this training bit)
    completed_trainingbits = list(user.trainingbits_completed.all().values_list('id', flat=True))
    suggested_trainingbits = trainingbits.exclude(id__in=completed_trainingbits)
    # 3 SQL queries

    return suggested_trainingbits

def get_completed_skills(user, trainingbit):
    completed_trainingbits = list(user.trainingbits_completed.all().values_list('id', flat=True))
    completed_skills = set([])
    possibly_completed_skills = trainingbit.skill_set.all().prefetch_related('trainingbits')

    # The query below saves us 1 SQL query by merging the user skills query
    # (in the line `completed_skills -= set(request.user.skills_completed.all())`)
    # with the training bit skills query, but it's almost unreadble
    #
    #    possibly_completed_skills = trainingbit.skill_set.exclude(pk__in=request.user.skills_completed.all().values('pk')).prefetch_related('trainingbits')

    for skill in possibly_completed_skills:
        skill_tbs =  skill.trainingbits.all() #cvalues_list('id', flat=True)).issubset(completed_trainingbits):
        # if set(skill.trainingbits.values_list('id', flat=True)).issubset(completed_trainingbits):
        if set(map(lambda t: t.pk, skill_tbs)).issubset(completed_trainingbits):
            completed_skills.add(skill)
    # 2 SQL queries
    completed_skills -= set(user.skills_completed.all())
    # 1 SQL query

    return completed_skills

@csrf_protect
def trainingbit_view(request, trainingbit_id):
    trainingbit_id = int(trainingbit_id)
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

            # complete trainingbit
            request.user.complete_trainingbit(trainingbit)

            suggested_trainingbits = get_suggested_trainingbits(request.user, request.session)
            completed_skills = get_completed_skills(request.user, trainingbit)
            print(completed_skills)

            # complete skills
            request.user.complete_skills(completed_skills)

            if request.is_ajax():
                modal_html = render_to_string('skills/partials/trainingbit_completed_modal.html', {
                    'trainingbit': trainingbit,
                    'suggested_trainingbits': suggested_trainingbits[:3],
                    'completed_skills': completed_skills,
                })
                project_html = render_to_string('partials/project_entry.html', {
                    'project': project,
                })
                # return rendered:
                # * completion dialog (modal_html)
                # * project for shared/projects section
                d = {
                    'modal_html': modal_html,
                    'project_html': project_html,
                }
                # The 201 HTTP status code is from my reading of the standard
                # the # correct response to a POST which successfully created a
                # new object.
                # See: http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.2
                return HttpResponse(json.dumps(d), content_type='application/json', status=201)
        else:
            if request.is_ajax():
                return HttpResponse(json.dumps(form.errors), content_type='application/json', status=404)



    return render(request, 'skills/trainingbit_view.html', {
        'trainingbit': trainingbit,
        'projects': trainingbit.project_set.prefetch_related('author'),
        'next': reverse('skills:trainingbit_view', args=[trainingbit_id]),
    })

@csrf_protect
def trainingbit_edit(request, trainingbit_id=None):

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

        selected_topic_pks = request.POST.getlist('topic-pks[]')
        selected_topic_pks = [int(s) for s in selected_topic_pks]
        topics = Topic.objects.filter(pk__in=selected_topic_pks)
        trainingbit.topic_set.clear()
        trainingbit.topic_set.add(*topics)

        # return HttpResponseRedirect(reverse('trainer_dashboard'))
        return HttpResponseRedirect(reverse('skills:trainingbit_edit_content', args=[trainingbit_id]))
            # return HttpResponseRedirect('/')
    elif trainingbit_id is not None:
        trainingbit = TrainingBit.objects.get(id__exact=trainingbit_id)
        selected_topic_pks = [t.pk for t in trainingbit.topic_set.all()]
    else:
        trainingbit = None
        selected_topic_pks = []


    # By default show training bit form
    return render(request, 'skills/trainingbit_edit.html', {
        'trainingbit': trainingbit,
        'topics': Topic.objects.all(),
        'selected_topic_pks': selected_topic_pks,
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


@csrf_protect
def topic_new(request):

    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            # Save
            topic = form.save()
            # messages.success(request, 'Project was successfully saved')

            if request.is_ajax():
                d = {'name': topic.name, 'deleteURL': reverse('skills:topic_delete', args=[topic.pk])}
                return HttpResponse(json.dumps(d), content_type='application/json', status=201)
            else:
                messages.success(request, 'Topic was successfully saved')
        else:
            if request.is_ajax():
                return HttpResponse(json.dumps(form.errors), content_type='application/json', status=404)

    return HttpResponseRedirect(reverse('trainer_dashboard'))

@csrf_protect
def topic_delete(request, topic_pk):
    topic = get_object_or_404(Topic, pk=topic_pk)

    # if request.method == 'POST':

    if request.user.has_perm('topic.delete', topic):
        topic.delete()
        if request.is_ajax():
            d = {'message': 'Topic was deleted'}
            return HttpResponse(json.dumps(d), content_type='application/json', status=201)
        else:
            messages.success(request, 'Topic was successfully deleted')
            return HttpResponseRedirect(reverse('trainer_dashboard'))
    else:
        # User doesn't have permission
        if request.is_ajax():
            return HttpResponse(json.dumps(form.errors), content_type='application/json', status=404)
        else:
            messages.error(request, 'You don\'t have permission to delete this topic')
            return HttpResponseRedirect(reverse('trainer_dashboard'))
