from django.db import models
from django.conf import settings

from taggit.managers import TaggableManager


LABELS = (
    ('inspiration', 'Inspiration'),
    ('background', 'Background'),
    ('doing', 'Doing'),
)


# Create your models here.
class TrainingBit(models.Model):
    name = models.CharField(max_length=30)
    label = models.CharField(max_length=16, choices=LABELS)
    description = models.TextField()
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


class Skill(models.Model):
    name = models.CharField(max_length=30)
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
