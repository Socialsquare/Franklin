from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager
from django.contrib.flatpages.models import FlatPage
from django.core.urlresolvers import reverse
from django.db.models import signals
from django.templatetags.static import static
from django.utils import timezone

from django.db import models
from allauth.account.models import EmailAddress
from django_countries.fields import CountryField

from skills.models import Skill, TrainingBit

# USERTYPES = (
#     ('user', 'User'),
#     ('trainer', 'Trainer'),
#     ('admin', 'Administrator'),
# )

class CustomUserManager(UserManager):

    def create_superuser(self, username, password, **kwargs):
        user = self.model(username=username, is_staff=True, is_superuser=True, **kwargs)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    # usertype = models.CharField(max_length=16, choices=USERTYPES, default='user')
    USERNAME_FIELD = 'username'

    # Metadata
    datetime_joined = models.DateTimeField(default=timezone.now)

    # Content
    username = models.CharField(max_length=40, unique=True, error_messages={
        'unique': 'The username you have choosen is already taken - please, pick another one'
    })
    # The error message on duplicate unique values cannot be set in forms
    # https://code.djangoproject.com/ticket/8913
    email = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='user-images', null=True, blank=True)
    description = models.TextField(blank=True)

    # Relations
    skills_in_progress = models.ManyToManyField(Skill, blank=True, related_name='users_in_progress')
    skills_completed = models.ManyToManyField(Skill, blank=True, related_name='users_completed')
    #   maybe another name for skills_completed?: skills_taken, skills_done

    #   Keep these names consistent with the ones above:
    #     skills_completed <-> trainingbits_completed
    trainingbits_in_progress = models.ManyToManyField(TrainingBit, blank=True, related_name='users_in_progress')
    trainingbits_completed = models.ManyToManyField(TrainingBit, blank=True, related_name='users_completed')

    # Flags
    is_active = models.BooleanField(default=True)
    has_been_welcomed = models.BooleanField(default=False)

    def is_taking_skill(self, skill):
        return skill in self.skills_in_progress.all()

    def complete_skill(self, completed_skill):
        skills = self.complete_skills([complete_skill])
        return skills[0]

    def complete_skills(self, completed_skills):
        self.skills_in_progress.remove(*completed_skills)
        self.skills_completed.add(*completed_skills)
        return completed_skills

    def has_completed_skill(self, skill):
        return skill in self.skills_completed.all()

    def is_taking_trainingbit(self, trainingbit):
        return trainingbit in self.trainingbits_in_progress.all()

    def complete_trainingbit(self, completed_trainingbit):
        tbs = self.complete_trainingbits([completed_trainingbit])
        return tbs[0]

    def complete_trainingbits(self, completed_trainingbits):
        self.trainingbits_in_progress.remove(*completed_trainingbits)
        self.trainingbits_completed.add(*completed_trainingbits)
        return completed_trainingbits

    def has_completed_trainingbit(self, trainingbit):
        return trainingbit in self.trainingbits_completed.all()

    # See: http://stackoverflow.com/questions/2771676/django-default-datetime-now-problem
    # this:
    #   from datetime import datetime
    #   date_joined = models.DateField(default=datetime.now)
    # or this:

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email


    objects = CustomUserManager()

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.get_primary(self.user)
            #result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False

    @property
    def is_trainer(self):
        if self.is_admin:
            return True
        return self.groups.filter(name='Trainers')

    @property
    def is_admin(self):
        return self.groups.filter(name='Admins') or self.is_superuser

    # is_staff = models.BooleanField()
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin or self.is_trainer

    def get_absolute_url(self):
        return reverse('profile', args=[self.id])

    def getImage(self):
        if self.image:
            return self.image.url
        else:
            return static('images/profile-picture-placeholder.png')

#signals.post_save.connect(update_allauth_primary_email, sender=User)


class UserInfo(models.Model):

    SEXES = [
        # (data representation, textual/user representation)
        ('female', 'Female'),
        ('male',   'Male'),
    ]
    ORGANISATION_TYPES = [
        ('org1', 'Organisation 1'),
        ('org2', 'Organisation 2'),
        ('org3', 'Organisation 3'),
        ('noorg', 'No organization'),
    ]

    # Content
    sex = models.CharField(max_length=20, choices=SEXES, blank=False)
    country = CountryField(null=True)
    birthdate = models.DateField(null=True)
    organization = models.CharField(max_length=15, choices=ORGANISATION_TYPES, blank=False)
    # Relations
    user = models.OneToOneField(User, null=True, blank=True)


# http://stackoverflow.com/a/10408140/118608
def get_or_create_userinfo(user):
    """
    Return the UserInfo for the given user, creating one if it does not exist.

    This will also set user.userinfo to cache the result.
    """
    userinfo, c = UserInfo.objects.get_or_create(user=user)
    # user.userinfo = userinfo  # Doesn't work (AttributeError: can't set attribute)
    return userinfo

User.userinfo = property(get_or_create_userinfo)

class GCLFlatPage(FlatPage):
    show_in_footer = models.BooleanField(default=False)
    class Meta:
        verbose_name = "flat page"
        verbose_name_plural = "flat pages"
    def get_absolute_url(self):
        return reverse('django.contrib.flatpages.views.flatpage', args=[self.url])

from solo.models import SingletonModel

class SiteConfiguration(SingletonModel):
    # site_name = models.CharField(max_length=255, default='Site Name')
    # maintenance_mode = models.BooleanField(default=False)
    analytics_code = models.TextField(help_text='Here you should paste the tracking code from Google Analytics, Clicky or another web traffic analysis platform. Including the &lt;script&gt; tags.')

    def __unicode__(self):
        return "Site Configuration (Google Analytics)"

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"
