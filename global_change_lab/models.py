from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager

from django.db import models
from allauth.account.models import EmailAddress

from skills.models import Skill

# USERTYPES = (
#     ('user', 'User'),
#     ('trainer', 'Trainer'),
#     ('admin', 'Administrator'),
# )


class User(AbstractBaseUser, PermissionsMixin):
    # usertype = models.CharField(max_length=16, choices=USERTYPES, default='user')
    USERNAME_FIELD = 'username'
    username = models.CharField(max_length=40, unique=True)
    email = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    skills_in_progress = models.ManyToManyField(Skill, related_name='sp')
    skills_taken = models.ManyToManyField(Skill, related_name='st')

    def is_taking_skill(self, skill):
        return skill in self.skills_in_progress.all()

    def has_taken_skill(self, skill):
        return skill in self.skills_taken.all()

    # See: http://stackoverflow.com/questions/2771676/django-default-datetime-now-problem
    # this:
    #   from datetime import datetime
    #   date_joined = models.DateField(default=datetime.now)
    # or this:
    date_joined = models.DateField(auto_now_add=True)

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email


    objects = UserManager()

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False

    def is_trainer(self):
        return self.groups.filter(name='Trainers')

    @property
    def is_admin(self):
        # return self.groups.filter(name='Admins')
        return self.is_staff

    # is_staff = models.BooleanField()
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser


