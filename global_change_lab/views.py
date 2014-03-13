from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

import django.contrib.messages as messages
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

from skills.models import Skill, TrainingBit, Topic, Image

from global_change_lab.models import User
from global_change_lab.forms import UserInfoForm

from django.db.models import Q
from datetime import datetime, timedelta

import csv, json

def front_page(request):
    if request.user.is_authenticated():
        return profile(request)

    return render(request, 'front_page.html', {
        'name': 'malthe',
        'skills': Skill.objects.all(),
    })

##### ONBOARDING VIEWS

def new_user(request):
    return render(request, 'new_user.html', {
    })

@csrf_protect
def new_user_input_details(request):
    form = None

    if request.POST:
        form = UserInfoForm(request.user, request.POST)

        if form.is_valid():
            userinfo = form.save()

            # request.user.userinfo = userinfo

            # request.user.description = form.description
            # request.user.save()

            return HttpResponseRedirect(reverse('new_user_topics'))

    else:
        form = UserInfoForm(request.user)

    return render(request, 'new_user_input_details.html', {
        'form': form
    })

def new_user_topics(request):
    return render(request, 'new_user_topics.html', {
      'topics': Topic.objects.all(),
    })


@csrf_protect
def new_user_suggestions(request):
    if request.method == 'POST':
        topic_ids = [int(pk) for pk in request.POST.getlist('topic_ids[]')]
        topics = Topic.objects.filter(id__in=topic_ids)
        print(topics)

        trainingbits = []
        skills = []
        for topic in topics[:4]:
            trainingbit_pks = [t.pk for t in trainingbits]
            trainingbits += topic.trainingbits.exclude(pk__in=trainingbit_pks)[:2]
            skill_pks = [t.pk for t in skills]
            skills += topic.skills.exclude(pk__in=skill_pks)[:2]
            # trainingbits += topic.trainingbits.all()[:2].distinct()
            # skills += topic.skills.all()[:2].distinct()

        if len(trainingbits) < 4:
            missing_count = 4 - len(trainingbits)
            trainingbits += TrainingBit.objects.all()[:missing_count]

        if len(skills) < 4:
            missing_count = 4 - len(skills)
            skills += Skill.objects.all()[:missing_count]

        return render(request, 'new_user_suggestions.html', {
            'trainingbits': trainingbits[:4],
            'skills': skills[:4],
        })
    else:
        return HttpResponseRedirect(reverse('new_user'))


# TODO: this page is a stub
def shares(request):
    return render(request, 'shares.html', {
        'shares': None, #Skill.objects.all(),
    })


from django.contrib import comments
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
def trainer_dashboard(request):
    all_trainingbits = request.user.trainingbit_set.all()
    trainingbits = filter(lambda t: not t.is_draft, all_trainingbits)
    trainingbit_drafts = filter(lambda t: t.is_draft, all_trainingbits)

    all_skills = request.user.skill_set.all()
    skills_public = filter(lambda s: s.is_public, all_skills)
    skills_hidden = filter(lambda s: not s.is_public, all_skills)

    return render(request, 'trainer_dashboard.html', {
        'trainingbits': trainingbits,
        'trainingbit_drafts': trainingbit_drafts,
        'skills_public': skills_public,
        'skills_hidden': skills_hidden,
        'topics': Topic.objects.all(),
    })

def statistics(request):
    return render(request, 'statistics.html', {
        'trainingbits': TrainingBit.objects.all(),
        'skills': Skill.objects.all(),
    })

def get_user_statistics():
    one_week_ago  = datetime.now() - timedelta(days = 7)
    one_month_ago = datetime.now() - timedelta(days = 30)
    one_year_ago  = datetime.now() - timedelta(days = 365)
    num_users_last_week  = len(User.objects.filter(datetime_joined__gt = one_week_ago  ).distinct())
    num_users_last_month = len(User.objects.filter(datetime_joined__gt = one_month_ago ).distinct())
    num_users_last_year  = len(User.objects.filter(datetime_joined__gt = one_year_ago  ).distinct())

    return {
        "num_users_last_week": num_users_last_week,
        "num_users_last_month": num_users_last_month,
        "num_users_last_year": num_users_last_year,
    }


def admin_dashboard(request):
    num_users = len(User.objects.distinct())
    template_dict = {
        "num_users": num_users,
    }
    template_dict.update(get_user_statistics())

    return render(request, 'admin_dashboard.html', template_dict)

def admin_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(["username", "datetime_joined", "name", "email", ])

    for user in User.objects.distinct():
        writer.writerow([user.username, user.datetime_joined, user.get_full_name(), user.email, ])

    return response

def admin_statistics_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="statistics.csv"'

    writer = csv.writer(response)
    writer.writerow(["num_users", 'num_users_last_week', 'num_users_last_month', 'num_users_last_year'])

    num_users = len(User.objects.distinct())

    d = get_user_statistics()

    writer.writerow([num_users, d['num_users_last_week'], d['num_users_last_month'], d['num_users_last_year']])

    return response


@login_required
@csrf_protect
def upload_picture(request):
    if request.method == 'POST':
        image = Image()
        image.image = request.FILES['picture']
        image.identifier = request.POST['identifier']
        image.author = request.user
        image.save()

        #generating json response array
        result = [
            {
                # "name"          : request.user.image.filename,
                # "size"          : file_size,
                "url" : image.image.url,
                # "thumbnail_url" : thumb_url,
                # "delete_url"    : file_delete_url+str(image.pk)+'/',
                # "delete_type"   : "POST",
            },
        ]
        response_data = json.dumps(result)
        return HttpResponse(response_data, mimetype='application/json')

    return HttpResponseRedirect(reverse('/'))

# @csrf_protect
def upload_profile_picture(request):
    print('did recieve')
    if request.method == 'POST':
        print('did post')
        request.user.image = request.FILES['profile-picture']
        request.user.save()
        print('did save')

        #generating json response array
        result = [
            {
                # "name"          : request.user.image.filename,
                # "size"          : file_size,
                "url"           : request.user.image.url,
                # "thumbnail_url" : thumb_url,
                # "delete_url"    : file_delete_url+str(image.pk)+'/',
                # "delete_type"   : "POST",
            },
        ]
        response_data = json.dumps(result)
        return HttpResponse(response_data, mimetype='application/json')

    return HttpResponseRedirect(reverse('profile'))


def profile(request, user_id=None):
    if user_id is None:
        profile_user = request.user
    else:
        profile_user = get_object_or_404(User, pk=user_id)

    newest_skills = profile_user.skills_completed.all()[:3]
    other_skills_count = profile_user.skills_completed.count() - 3

    if request.user == profile_user:
        own_profile = True

        trainingbits_completed = request.user.trainingbits_completed.values_list('pk', flat=True)

        skills_in_progress_w_percentage = []
        skills_in_progress = request.user.skills_in_progress.prefetch_related('trainingbits').all()
        for skill in skills_in_progress:
            tbs = skill.trainingbits.all()
            incompleted_count = len(set([t.pk for t in tbs]) - set(trainingbits_completed))
            total_count = len(tbs)
            if total_count == 0:
                percentage = 0
            else:
                percentage = 1.0 - (incompleted_count / total_count)
                percentage *= 100
            skill.percentage = percentage
            skills_in_progress_w_percentage.append((skill, int(percentage)))

        trainingbits_in_progress = request.user.trainingbits_in_progress.all()

        in_progress_dict = {
            'skills_in_progress_w_percentage': skills_in_progress_w_percentage,
            'skills_in_progress': skills_in_progress,
            'trainingbits_in_progress': trainingbits_in_progress,
        }
    else:
        own_profile = False
        in_progress_dict = {}

    projects = list(profile_user.project_set.order_by('-created_at').select_related('trainingbit').prefetch_related('comment_set').all()[:12])
    project_list0 = projects[0::3]
    project_list1 = projects[1::3]
    project_list2 = projects[2::3]

    template_dict = {
        'own_profile': own_profile,
        'profile_user': profile_user,
        'newest_skills': newest_skills,
        'other_skills_count': other_skills_count,
        'project_list0': project_list0,
        'project_list1': project_list1,
        'project_list2': project_list2,
        'hide_comments': True,
    }
    template_dict.update(in_progress_dict)

    return render(request, 'profile.html', template_dict)


def user_list(request):
    # `datetime_joined`  means ascending
    # `-datetime_joined` means descending
    # `+datetime_joined` doesn't exist and will result in an error(!)
    new_users = User.objects.all().order_by('-datetime_joined')
    print(new_users)

    return render(request, 'user_list.html', {
        'new_users': new_users,
    })


def user_delete(request, user_id):
    user = User.objects.get(id__exact=user_id)

    if user == request.user:
        user.delete()
        messages.success(request, 'Successfully deleted your user.')
    else:
        messages.error(request, 'You do not have permissions to delete this user.')



    return HttpResponseRedirect(reverse('front_page'))


def user_upgrade_to_trainer(request, user_id):
    user = User.objects.get(id__exact=user_id)

    if request.user.is_admin:
        g = Group.objects.get(name='Trainers')
        g.user_set.add(user)

        messages.success(request, 'Successfully upgraded %s to be a trainer.' % user.username)
    else:
        messages.error(request, 'You do not have permissions to upgrade this user.')

    return HttpResponseRedirect(reverse('profile', args=[user_id]))

@csrf_protect
def page_new(request):

    if request.method == 'POST':
        flatpage = FlatPage()
        flatpage.url = '/' + request.POST['title'].replace(' ', '-').lower() + '/'
        flatpage.title = request.POST['title']
        flatpage.content = request.POST['content']
        flatpage.save()
        flatpage.sites.add(*Site.objects.all())
        messages.success(request, 'Successfully created page "%s"' % flatpage.title)

        return HttpResponseRedirect(reverse('django.contrib.flatpages.views.flatpage', args=[flatpage.url]))
    else:
        return HttpResponseRedirect(reverse('trainer_dashboard'))

@csrf_protect
def page_delete(request, page_pk):

    page = get_object_or_404(FlatPage, pk=page_pk)
    page.delete()
    messages.success(request, 'Successfully deleted page "%s"' % page.title)
    return HttpResponseRedirect(reverse('trainer_dashboard'))

    # return HttpResponseRedirect(reverse('django.contrib.flatpages.views.flatpage', args=[flatpage.url]))
