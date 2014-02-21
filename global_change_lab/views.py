from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404

import django.contrib.messages as messages
from django.contrib.auth.models import Group

from skills.models import Skill, TrainingBit

from global_change_lab.models import User
from django.db.models import Q
from datetime import datetime, timedelta

import csv

def front_page(request):
    return render(request, 'front_page.html', {
        'name': 'malthe',
        'skills': Skill.objects.all(),
    })

def new_user(request):
    return render(request, 'new_user.html', {
    })


# TODO: this page is a stub
def shares(request):
    return render(request, 'shares.html', {
        'shares': None, #Skill.objects.all(),
    })


def trainer_dashboard(request):
    return render(request, 'trainer_dashboard.html', {
        'trainingbits': request.user.trainingbit_set.all(),
        'skills': request.user.skill_set.all(),
        # TrainingBit.objects.l
        # 'shares': None, #Skill.objects.all(),
    })

def trainingbit_statistics(request):
    return render(request, 'trainingbit_statistics.html', {
        'trainingbits': TrainingBit.objects.all(),
    })

def skill_statistics(request):
    return render(request, 'skill_statistics.html', {
        'skills': Skill.objects.all(),
    })

def admin_dashboard(request):
    num_users = len(User.objects.distinct())
    
    one_month_ago = datetime.now() - timedelta(days=30)
    num_users_last_month = len(User.objects.filter(date_joined__gt=one_month_ago  ).distinct())
    
    return render(request, 'admin_dashboard.html', {
        "num_users": num_users,
        "num_users_last_month": num_users_last_month,
        })

def admin_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    
    writer = csv.writer(response)
    writer.writerow(["username", "date_joined", "name", "email", ])

    for user in User.objects.distinct():
        writer.writerow([user.username, user.date_joined, user.get_full_name(), user.email, ])
    
    return response

def admin_statistics_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="statistics.csv"'
    
    writer = csv.writer(response)
    writer.writerow(["num_users", "num_users_last_month"])

    num_users = len(User.objects.distinct())
    
    one_month_ago = datetime.now() - timedelta(days=30)
    num_users_last_month = len(User.objects.filter(date_joined__gt=one_month_ago  ).distinct())

    writer.writerow([num_users, num_users_last_month])

    return response
    
    
def user_progress(request):
    if request.user.is_authenticated:
        return render(request, 'user_progress.html', {})
    else:
        return HttpResponseRedirect(reverse('login'))


def profile(request, user_id=None):
    if user_id is None:
        user = request.user
    else:
        user = get_object_or_404(User, pk=user_id)
    return render(request, 'profile.html', {
        'some_user': user,
        'user_fields': User._meta.get_all_field_names(),
    })


def user_list(request):
    # `date_joined`  means ascending
    # `-date_joined` means descending
    # `+date_joined` doesn't exist and will result in an error(!)
    new_users = User.objects.all().order_by('-date_joined')
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
