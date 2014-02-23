from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager
from django.core.urlresolvers import reverse

from django.db import models
from allauth.account.models import EmailAddress

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
    username = models.CharField(max_length=40, unique=True)
    email = models.CharField(max_length=100)
    image = models.ImageField(upload_to='trainingbits', null=True)
    description = models.TextField(blank=True)

    skills_in_progress = models.ManyToManyField(Skill, blank=True, related_name='users_in_progress')
    skills_completed = models.ManyToManyField(Skill, blank=True, related_name='users_completed')
    # maybe another name for skills_completed?: skills_taken, skills_done

    # Keep these name consistent with the ones above
    #   skills_completed <-> trainingbits_completed
    trainingbits_in_progress = models.ManyToManyField(TrainingBit, blank=True, related_name='users_in_progress')
    trainingbits_completed = models.ManyToManyField(TrainingBit, blank=True, related_name='users_completed')

    is_active = models.BooleanField(default=True)

    def is_taking_skill(self, skill):
        return skill in self.skills_in_progress.all()

    def has_completed_skill(self, skill):
        return skill in self.skills_completed.all()

    def is_taking_trainingbit(self, trainingbit):
        return trainingbit in self.trainingbits_in_progress.all()

    def has_completed_trainingbit(self, trainingbit):
        return trainingbit in self.trainingbits_completed.all()

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


    objects = CustomUserManager()

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

    def get_absolute_url(self):
        return reverse('profile', args=[self.id])

    def getImage(self):
        if self.image:
            return self.image.url
        else:
            return 'defaultimage'


from solo.models import SingletonModel

class SiteConfiguration(SingletonModel):
    # site_name = models.CharField(max_length=255, default='Site Name')
    # maintenance_mode = models.BooleanField(default=False)
    analytics_code = models.TextField(help_text='Here you should paste the tracking code from Google Analytics, Clicky or another web traffic analysis platform. Including the &lt;script&gt; tags.')

    def __unicode__(self):
        return u"Site Configuration (Google Analytics)"

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"
