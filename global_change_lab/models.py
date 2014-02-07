from django.contrib.auth.models import User
from django.db import models
from allauth.account.models import EmailAddress

# USERTYPES = (
#     ('user', 'User'),
#     ('trainer', 'Trainer'),
#     ('admin', 'Administrator'),
# )


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    # usertype = models.CharField(max_length=16, choices=USERTYPES, default='user')

    def __unicode__(self):
        return "{}'s profile".format(self.user.username)

    class Meta:
        db_table = 'user_profile'

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False

    def is_trainer(self):
        return self.user.groups.filter(name='Trainers')


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
