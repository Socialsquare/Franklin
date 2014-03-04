from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect

import django.contrib.messages as messages
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

from skills.models import Skill, TrainingBit, Topic

from global_change_lab.models import User
from django.db.models import Q
from datetime import datetime, timedelta

import csv, json

def front_page(request):
    return render(request, 'front_page.html', {
        'name': 'malthe',
        'skills': Skill.objects.all(),
    })

def new_user(request):
    return render(request, 'new_user.html', {
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

    return render(request, 'trainer_dashboard.html', {
        'trainingbits': request.user.trainingbit_set.all(),
        'skills': request.user.skill_set.all(),
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


def user_progress(request):
    if request.user.is_authenticated:
        return render(request, 'user_progress.html', {})
    else:
        return HttpResponseRedirect(reverse('login'))


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
        user = request.user
    else:
        user = get_object_or_404(User, pk=user_id)

    newest_skills = user.skills_completed.all()[:3]
    other_skills_count = user.skills_completed.count() - 3

    return render(request, 'profile.html', {
        'some_user': user,
        'user_fields': User._meta.get_all_field_names(),
        'newest_skills': newest_skills,
        'other_skills_count': other_skills_count,
    })


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

    if request.user.profile.is_admin():
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
