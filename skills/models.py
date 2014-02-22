from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from taggit.managers import TaggableManager
from datetime import datetime


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ['skills.models.AutoDateTimeField'])
# Don't use `auto_now` and `auto_now_add`:
#   http://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add/1737078#1737078
#   https://groups.google.com/forum/#!topic/django-developers/TNYxwiXLTlI
class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return datetime.now()


# Create your models here.
class TrainingBit(models.Model):
    LABELS = (
        ('I', 'Inspiration'),
        ('B', 'Background'),
        ('T', 'Tool'),
    )

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = AutoDateTimeField()

    label = models.CharField(max_length=1, choices=LABELS, null=False, blank=False)
    description = models.TextField()
    json_content = models.TextField(default='{"learn":[],"act":[],"share":[]}')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    recommended = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)

    tags = TaggableManager()

    image = models.ImageField(upload_to='trainingbits', default='defaultimage', null=False)

    def getImage(self):
        if self.image:
            return self.image.url
        else:
            return 'defaultimage'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('skills:trainingbit_view', args=[self.id])


class Skill(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = AutoDateTimeField()
    # optional relation to training bits (i.e. a skill does _have_ to have a
    # training bit)
    trainingbits = models.ManyToManyField(TrainingBit, blank=True, null=True)
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    is_public = models.BooleanField(default=True)

    tags = TaggableManager()

    image = models.ImageField(upload_to='trainingbits', default='defaultimage', null=False)

    def getImage(self):
        if self.image:
            return self.image.url
        else:
            return 'defaultimage'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('skills:skill_view', args=[self.id])


class Project(models.Model):
    # Metadata
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = AutoDateTimeField()

    # Content
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='trainingbits', null=True)

    # Relations
    trainingbit = models.ForeignKey(TrainingBit, null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    # Flags
    is_public = models.BooleanField(default=True)

    # def getImage(self):
    #     if self.image:
    #         return self.image.url
    #     else:
    #         return ''

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('skills:trainingbit_view', args=[self.trainingbit.id]) + \
               '#project-%u' % self.id

# apply AuthorPermissionLogic and CollaboratorsPermissionLogic
from permission import add_permission_logic
from permission.logics import PermissionLogic, AuthorPermissionLogic
# from permission.logics import CollaboratorsPermissionLogic

# Authors have full permission (edit, delete etc.) to their own skills and training bits
add_permission_logic(Skill, AuthorPermissionLogic())
add_permission_logic(TrainingBit, AuthorPermissionLogic())

class AdminPermissionLogic(PermissionLogic):
    def has_perm(user, permission_str, obj):
        if user.is_admin():
            return True
        else:
            return False

# Admin always have full permission
add_permission_logic(Skill, AdminPermissionLogic())
add_permission_logic(TrainingBit, AdminPermissionLogic())
