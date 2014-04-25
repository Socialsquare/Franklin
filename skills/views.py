from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType

import django.contrib.messages as messages
from permission.decorators import permission_required

from skills.models import Skill, TrainingBit, Topic, Project, Comment, Like
from skills.forms import SkillForm, TrainingBitForm, ProjectForm, CommentForm, TopicForm, LikeForm

from django_sortable.helpers import sortable_helper

import json

def fetch_data_for_columns(projects, comments):
    all_projects = list(projects.order_by('-created_at')[:12])
    project_list0 = all_projects[0::2]
    project_list1 = all_projects[1::2]

    latest_comments = comments.exclude(is_deleted__exact=True).\
        prefetch_related('author', 'project').order_by('-created_at')[:9]

    return {
        'project_list0': project_list0,
        'project_list1': project_list1,
        'comments': latest_comments
    }

def shares_overview(request):
    if request.is_ajax():
        i_project = int(request.GET['project_page_last'])
        i_comment = int(request.GET['comment_page_last'])

        projects = Project.objects.filter(is_deleted=False).order_by('-created_at')[i_project:i_project+12]
        comments = Comment.objects.exclude(is_deleted__exact=True).prefetch_related('author', 'project').order_by('-created_at')[i_comment:i_comment+9]

        rendered_projects = [render_to_string('skills/partials/project_column.html', {'project': p}) for p in projects]
        rendered_comments = [render_to_string('skills/partials/comment_entry_compact.html', {'comment': c}) for c in comments]

        d = {
            'html_projects':  rendered_projects,
            'html_comments':  rendered_comments,
            'project_page_last': i_project+12,
            'comment_page_last': i_comment+9,
        }

        return HttpResponse(json.dumps(d), content_type='application/json', status=201)
    else:
        return render(request, 'skills/shares_overview.html', {
            'projects': Project.objects.filter(is_deleted=False).order_by('-created_at')[:12],
            'comments': Comment.objects.exclude(is_deleted__exact=True).prefetch_related('author', 'project').order_by('-created_at')[:9],
        })


def skills_overview(request, topic_slug=None, show_drafts=False, show_recommended=False):
    # Show from topic
    if topic_slug is not None:
        topic = get_object_or_404(Topic, slug=topic_slug)
        skills = topic.skills.all()
    else:
        topic = None
        skills = Skill.objects.all()

    # Show recommended
    if show_recommended:
        skills = skills.filter(is_recommended=True)

    # Show public/drafts
    if request.user.is_trainer and show_drafts:
        skills = skills.filter(is_draft=True)
    else:
        # by default show the skill that are _not_ drafts
        # that is - show the public skills
        skills = skills.filter(is_draft=False)

    # Sort
    skills = sortable_helper(request, skills)

    return render(request, 'skills/skills_overview.html', {
        'skills': skills,
        'showing_drafts': show_drafts,
        'showing_recommended': show_recommended,
        'topics': Topic.objects.all(),
        'topic_chosen': topic,
    })

def skill_view(request, slug=None):
    skill = get_object_or_404(Skill, slug=slug)

    trainingbits = skill.trainingbits.filter(is_draft__exact=False)
    trainingbit_pks = [t.id for t in trainingbits]
    project_count = Project.objects.filter(is_deleted=False, trainingbit_id__in=trainingbit_pks).count()

    # Like
    content_type = ContentType.objects.get_for_model(skill)
    user_like = None
    try:
        if request.user.is_authenticated():
            user_like = request.user.like_set.get(object_id=skill.pk, content_type=content_type)
    except Like.DoesNotExist:
        pass


    return render(request, 'skills/skill_view.html', {
        'user_like': user_like,
        'content_type': content_type,
        'likes': skill.likes.count(),
        'skill': skill,
        'skill_id_get_query': '?skill_id=%u' % skill.id,
        'trainingbits': trainingbits,
        'project_count': project_count,
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

    return HttpResponseRedirect(skill.get_absolute_url())

@csrf_protect
def skill_stop(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)

    request.user.skills_in_progress.remove(skill)
    messages.info(request, 'You are no longer taking this skill')

    return HttpResponseRedirect(skill.get_absolute_url())

@csrf_protect
#@permission_required('skill.publicize')
def skill_publicize(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    if request.user.has_perm('skill.publicize', skill):
        if skill.is_draft:
            skill.is_draft = False
            messages.info(request, 'The skill is now public')
        else:
            skill.is_draft = True
            messages.success(request, 'Reverted skill to draft status')
        skill.save()
    else:
        messages.error(request, 'You do not have permission to make this skill public')

    return HttpResponseRedirect(skill.get_absolute_url())

def skill_delete(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    if  request.user.has_perm('skill.delete', skill):
        skill.delete()
        messages.success(request, 'The skill was deleted')
        return HttpResponseRedirect(reverse('skills:skills_overview'))
    else:
        messages.error(request, 'You do not have permission to delete this skill')
        return HttpResponseRedirect(skill.get_absolute_url())

@csrf_protect
def skill_edit(request, slug=None):

    skill = None
    selected_topic_pks = []
    form = SkillForm()

    if slug is not None:
        skill = get_object_or_404(Skill, slug=slug)
        selected_topic_pks = [t.pk for t in skill.topic_set.all()]
        form = SkillForm(instance=skill)


    # If something has been uploaded
    if request.method == 'POST':

        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():

            skill = form.save(commit=False)
            skill.author = request.user
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

            return HttpResponseRedirect(reverse('skills:skill_edit', args=[skill.slug]))
        else:
            messages.error(request, 'Could not save skill %s ' % form.errors)

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
        'form': form,
    })


def trainingbits_overview(request, topic_slug=None, show_recommended=False):
    if topic_slug is not None:
        topic = get_object_or_404(Topic, slug=topic_slug)
        trainingbits = topic.trainingbits.all()
    else:
        topic = None
        trainingbits = TrainingBit.objects.all()


    # Show recommended
    if show_recommended:
        trainingbits = trainingbits.filter(is_recommended=True)

    trainingbits = trainingbits.filter(is_draft__exact=False)
    trainingbits = sortable_helper(request, trainingbits)
    return render(request, 'skills/trainingbits_overview.html', {
        'trainingbits': trainingbits,
        'topics': Topic.objects.all(),
        'topic_chosen': topic,
        'showing_recommended': show_recommended,
    })

def trainingbit_cover(request, slug=None):
    trainingbit = get_object_or_404(TrainingBit, slug=slug)

    # Remember what skill the user came from and save it as the user's "current
    # skill".
    try:
        skill_id = request.GET['skill_id']
        request.session['current_skill_id'] = skill_id
    except KeyError:
        pass

    # If the user has a current skill let the user go back to that skill.
    back_url = None
    if request.session.get('current_skill_id') is not None:
        skill = Skill.objects.get(id__exact=request.session.get('current_skill_id'))
        if skill is not None:
            back_url = skill.get_absolute_url()

    # Like
    content_type = ContentType.objects.get_for_model(trainingbit)
    user_like = None
    try:
        if request.user.is_authenticated():
            user_like = request.user.like_set.get(object_id=trainingbit.pk, content_type=content_type)
    except Like.DoesNotExist:
        pass

    # Related trainingbits
    topic_pks = trainingbit.topic_set.all().values('id')
    related_trainingbits = TrainingBit.objects.filter(topic__id__in=topic_pks).distinct()

    template_vars = {
        'trainingbit': trainingbit,
        'content_type': content_type,
        'user_like': user_like,
        'projects': trainingbit.project_set.filter(is_deleted=False).prefetch_related('author').prefetch_related('comment_set'),
        'related_trainingbits': related_trainingbits[:4],
        'current_skill_id': request.session.get('current_skill_id'),
        'back_url': back_url,
    }
    project_pks = list(trainingbit.project_set.filter(is_deleted=False).values_list('pk', flat=True))
    comments = Comment.objects.filter(pk__in=project_pks)
    template_vars.update(fetch_data_for_columns(trainingbit.project_set, comments))

    return render(request, 'skills/trainingbit_cover.html', template_vars)

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

@login_required
@csrf_protect
def trainingbit_view(request, slug=None):
    trainingbit = get_object_or_404(TrainingBit, slug=slug)

    form = ProjectForm()

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
            request.session['completed_trainingbit_pk'] = trainingbit.pk

            # complete skills
            completed_skills = get_completed_skills(request.user, trainingbit)
            request.user.complete_skills(completed_skills)
            request.session['completed_skill_pks'] = [s.pk for s in completed_skills]

            return HttpResponseRedirect(project.get_absolute_url())
        else:
            if request.is_ajax():
                return HttpResponse(json.dumps(form.errors), content_type='application/json', status=404)



    return render(request, 'skills/trainingbit_view.html', {
        'trainingbit': trainingbit,
        'projects': trainingbit.project_set.filter(is_deleted=False).order_by('-created_at').prefetch_related('author'),
        'next': reverse('skills:trainingbit_view', kwargs={'slug': trainingbit.slug}),
        'back_url': reverse('skills:trainingbit_cover', kwargs={'slug': trainingbit.slug}),
        'form': form,
    })

@csrf_protect
def trainingbit_edit(request, slug=None):

    trainingbit = None
    selected_topic_pks = []


    if slug is not None:
        trainingbit = get_object_or_404(TrainingBit, slug=slug)
        selected_topic_pks = [t.pk for t in trainingbit.topic_set.all()]

    form = TrainingBitForm(instance=trainingbit)

    # If something has been uploaded
    if request.method == 'POST':

        form = TrainingBitForm(request.POST, request.FILES, instance=trainingbit)
        if form.is_valid():

            new_trainingbit = form.save(commit=False)
            try:
                if new_trainingbit.image == '' and trainingbit is not None and trainingbit.image != '':
                    new_trainingbit.image = trainingbit.image
            except NameError:
                pass
            new_trainingbit.author = request.user

            new_trainingbit.save()
            trainingbit = new_trainingbit
            trainingbit_id = trainingbit.id

            selected_topic_pks = request.POST.getlist('topic-pks[]')
            selected_topic_pks = [int(s) for s in selected_topic_pks]
            topics = Topic.objects.filter(pk__in=selected_topic_pks)
            trainingbit.topic_set.clear()
            trainingbit.topic_set.add(*topics)
        else:
            messages.error(request, 'Could not save training bit %s' % form.errors)

    # By default show training bit form
    return render(request, 'skills/trainingbit_edit.html', {
        'trainingbit': trainingbit,
        'topics': Topic.objects.all(),
        'selected_topic_pks': selected_topic_pks,
        'labels': TrainingBit.LABELS,
        'form': form,
    })

@csrf_protect
def trainingbit_edit_content(request, slug=None):
    trainingbit = get_object_or_404(TrainingBit, slug=slug)

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
        'back_url': reverse('skills:trainingbit_edit', kwargs={'slug': trainingbit.slug}),
    })

@csrf_protect
def trainingbit_delete(request, trainingbit_pk):
    trainingbit = get_object_or_404(TrainingBit, pk=trainingbit_pk)
    if request.user.has_perm('trainingbit.delete', trainingbit):
        trainingbit.delete()
        return HttpResponseRedirect(reverse('skills:trainingbits_overview'))
    else:
        return HttpResponseRedirect(trainingbit.get_absolute_url())

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
        if trainingbit.is_recommended:
            trainingbit.is_recommended = False
            messages.info(request, 'The training bit is no longer recommended')
        else:
            trainingbit.is_recommended = True
            messages.success(request, 'Successfully recommended training bit')
        trainingbit.save()
        return HttpResponseRedirect(trainingbit.get_absolute_url())
    else:
        messages.error(request, 'You do not have permission to recommend this training bit')
        return HttpResponseRedirect(trainingbit.get_absolute_url())

@csrf_protect
def skill_recommend(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    if request.user.has_perm('skill.recommend', skill):
        if skill.is_recommended:
            skill.is_recommended = False
            messages.info(request, 'The skill is no longer recommended')
        else:
            skill.is_recommended = True
            messages.success(request, 'Successfully recommended skill')
        skill.save()
        return HttpResponseRedirect(skill.get_absolute_url())
    else:
        messages.error(request, 'You do not have permission to recommend this skill')
        return HttpResponseRedirect(skill.get_absolute_url())

@login_required
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

    return HttpResponseRedirect(reverse('skills:trainingbit_view', kwargs={'slug': trainingbit.slug}))

@csrf_protect
def trainingbit_stop(request, trainingbit_id):
    trainingbit = get_object_or_404(TrainingBit, pk=trainingbit_id)

    request.user.trainingbits_in_progress.remove(trainingbit)
    messages.info(request, 'You are no longer taking this training bit')

    return HttpResponseRedirect(trainingbit.get_absolute_url())


@csrf_protect
def topic_new(request):

    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            # Save
            topic = form.save(commit=False)
            topic.author = request.user
            topic.slug = slugify(topic.name)
            topic.save()
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


def project_view(request, slug=None):
    project = get_object_or_404(Project, slug=slug, is_deleted=False)

    ### Suggestion modal
    completed_trainingbit_pk = request.session.get('completed_trainingbit_pk')
    if completed_trainingbit_pk is not None:
        # There's no hard guarantee that we are on the project that the user
        # recently completed a training bit through, but we assume it here:
        #   If the session variable is set - we show the suggestions and
        #   congratulations regardless of what project page we are on.
        show_suggestions = True
        suggested_trainingbits = get_suggested_trainingbits(request.user, request.session)
        completed_skill_pks = request.session.get('completed_skill_pks')
        completed_skills = Skill.objects.filter(pk__in=completed_skill_pks)

        # Remove "recently completed" state from session
        request.session.pop('completed_trainingbit_pk')
        request.session.pop('completed_skill_pks')
    else:
        show_suggestions = False
        suggested_trainingbits = []
        completed_skills = []

    # Like
    content_type = ContentType.objects.get_for_model(project)
    user_like = None
    try:
        if request.user.is_authenticated():
            user_like = request.user.like_set.get(object_id=project.pk, content_type=content_type)
    except Like.DoesNotExist:
        pass

    # Related projects
    related_projects = list(project.trainingbit.project_set.exclude(pk__exact=project.pk, is_deleted=True)[:3])
    related_project1 = None
    related_project2 = None
    related_project3 = None
    try:
        related_project1 = related_projects[0]
        related_project2 = related_projects[1]
        related_project3 = related_projects[2]
    except IndexError:
        pass


    return render(request, 'skills/project_view.html', {
        'user_like': user_like,
        'content_type': content_type,
        'project': project,
        'comments': project.root_comments().order_by('-created_at').prefetch_related('author'),
        'next': project.get_absolute_url(),
        'back_url': project.trainingbit.get_absolute_url(),

        'related_project1': related_project1,
        'related_project2': related_project2,
        'related_project3': related_project3,

        'suggested_trainingbits': suggested_trainingbits[:3],
        'completed_skills': completed_skills,
        'show_suggestions': show_suggestions,
    })


@login_required
def project_flag(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    project.is_flagged = True
    project.save()
    messages.success(request, 'Project was successfully flagged')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def project_delete(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.user.has_perm('skills.project_delete', project):
        project.is_deleted = True
        project.save()
        messages.success(request, 'Project was successfully deleted')
    else:
        messages.success(request, 'You do not have permissions to delete this project')

    return HttpResponseRedirect(reverse('front_page'))


@csrf_protect
def comment_post(request):
    if request.method == 'POST': # If the form has been submitted...
        form = CommentForm(request.POST)
        if form.is_valid():
            # Save
            comment = form.save(commit=False)
            comment.author = request.user
            project = comment.project
            print(request.POST)
            if 'parent_pk' in request.POST:
                comment.parent = Comment.objects.get(pk__exact=request.POST['parent_pk'])
            # comment.project = project
            comment.save()
            if request.is_ajax():
                comment_html = render_to_string('skills/partials/comment_entry.html', {
                    'comment': comment,
                })
                # return rendered:
                # * comment
                d = {
                    'comment_html': comment_html,
                }
                # The 201 HTTP status code is from my reading of the standard
                # the # correct response to a POST which successfully created a
                # new object.
                # See: http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.2
                return HttpResponse(json.dumps(d), content_type='application/json', status=201)
            else:
                messages.success(request, 'Comment was successfully saved')
        else:
            messages.error(request, 'Comment could not be saved: %s' % form.errors)

        try:
            return HttpResponseRedirect(project.get_absolute_url())
        except UnboundLocalError:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponseRedirect(reverse('front_page'))


@login_required
def comment_flag(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.is_flagged = True
    comment.save()
    messages.success(request, 'Comment was successfully flagged')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def comment_unflag(request, comment_pk):
    if request.user.is_admin:
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.is_flagged = False
        comment.save()
        messages.success(request, 'Comment was successfully unflagged')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.is_deleted = True
    comment.save()
    messages.success(request, 'Comment was successfully deleted')

    return HttpResponseRedirect(reverse('front_page'))


@login_required
@csrf_protect
def like(request):
    if request.method == 'POST':  # If the form has been submitted...
        like = Like.objects.filter(object_id=request.POST['object_id'],
                                   content_type=request.POST['content_type'],
                                   author__pk=request.user.pk)
        print(len(like))
        if like.exists():
            like.delete()
            if request.is_ajax():
                d = {'success': 'SUCCESS!!!!11'}
                return HttpResponse(json.dumps(d), content_type='application/json', status=201)
            else:
                messages.info(request, 'You no longer like this %s' % like.content_type)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            like = Like(author=request.user)
            form = LikeForm(request.POST, instance=like)
            if form.is_valid():
                like = form.save(commit=False)
                like.author = request.user
                like.save()
                if request.is_ajax():
                    d = {'success': 'SUCCESS!!!!11'}
                    return HttpResponse(json.dumps(d), content_type='application/json', status=201)
                else:
                    messages.success(request, 'Like absorbed')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, 'Form invalid %s' % form.errors)
                return HttpResponse(json.dumps(form.errors), content_type='application/json', status=404)
    else:
        messages.error(request, 'Did not like')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
