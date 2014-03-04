from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from sortedm2m.fields import SortedManyToManyField

from datetime import datetime


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ['skills.models.AutoDateTimeField'])

#### ABSTRACT MODELS (for inclusion via inheritance)
# Don't use `auto_now` and `auto_now_add`:
#   http://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add/1737078#1737078
#   https://groups.google.com/forum/#!topic/django-developers/TNYxwiXLTlI
class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return datetime.now()


# Please have this model as a parent for your models if you want to have the
# fields:
# * created_at
# * updated_at
# in your model
class TimedModel(models.Model):
    # Metadata
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = AutoDateTimeField()

    class Meta:
        abstract = True


# Please have this model as a parent for your models if you want the model to
# have an author.
class AuthoredModel(models.Model):
    # Relations
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False)

    class Meta:
        abstract = True


#### CONCRETE MODELS
class TrainingBit(TimedModel, AuthoredModel):
    LABELS = (
        ('I', 'Inspiration'),
        ('B', 'Background'),
        ('T', 'Tool'),
    )

    # Content
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='trainingbits', default='defaultimage')
    label = models.CharField(max_length=1, choices=LABELS, blank=False)
    json_content = models.TextField(default='{"learn":[],"act":[],"share":[]}')

    # Flags
    recommended = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)

    def getImage(self):
        if self.image:
            return self.image.url
        else:
            return 'defaultimage'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('skills:trainingbit_cover', args=[self.id])


class Project(TimedModel, AuthoredModel):

    # Content
    name = models.CharField(max_length=100, blank=False)
    content = models.TextField(blank=False)
    image = models.ImageField(upload_to='trainingbits', blank=True)
    link = models.URLField(blank=True)

    # Relations
    trainingbit = models.ForeignKey(TrainingBit, blank=False)

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


class Comment(TimedModel, AuthoredModel):

    # Content
    text = models.TextField(blank=True)

    # Relations
    project = models.ForeignKey(Project)
    parent = models.ForeignKey('self', blank=True, null=True)
    #  you cannot write ForeignKey(Comment)
    #  as Comment hasn't been defined yet
    #  See: https://docs.djangoproject.com/en/1.6/ref/models/fields/#foreignkey

    # Flags
    is_flagged = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_hidden  = models.BooleanField(default=False)


class Skill(TimedModel, AuthoredModel):

    # Content
    name = models.CharField(max_length=30)
    description = models.TextField()

    # Relations
    #   optional relation to training bits (i.e. a skill does _have_ to have a
    #   training bit)
    trainingbits = SortedManyToManyField(TrainingBit, blank=True)

    # Flags
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('skills:skill_view', args=[self.id])


class Topic(TimedModel, AuthoredModel):

    # Content
    name = models.CharField(max_length=100, blank=False, unique=True)

    # Semantic URLs
    slug = models.CharField(max_length=100, blank=False, unique=True)

    # Relations
    trainingbits = models.ManyToManyField(TrainingBit, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)

    def clean(self):
        # always be lowercase
        self.name = self.name.lower()

    def __str__(self):
        return self.name


# apply AuthorPermissionLogic and CollaboratorsPermissionLogic
from permission import add_permission_logic
from permission.logics import PermissionLogic, AuthorPermissionLogic
# from permission.logics import CollaboratorsPermissionLogic

# Authors have full permission (edit, delete etc.) to their own skills and training bits
add_permission_logic(Skill, AuthorPermissionLogic())
add_permission_logic(TrainingBit, AuthorPermissionLogic())
add_permission_logic(Project, AuthorPermissionLogic())
add_permission_logic(Comment, AuthorPermissionLogic())

class AdminPermissionLogic(PermissionLogic):
    def has_perm(user, permission_str, obj):
        if user.is_admin():
            return True
        else:
            return False

# Admin always have full permission
add_permission_logic(Skill, AdminPermissionLogic())
add_permission_logic(TrainingBit, AdminPermissionLogic())
add_permission_logic(Comment, AdminPermissionLogic())
