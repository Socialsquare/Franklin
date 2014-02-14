from django.db import models
from django.contrib.auth.models import User

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
    author = models.ForeignKey(User)
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
    training_bits = models.ManyToManyField(TrainingBit, blank=True, null=True)
    description = models.TextField()
    author = models.ForeignKey(User)

    tags = TaggableManager()

    image = models.ImageField(upload_to='trainingbits', default='defaultimage', null=False)

    def getImage(self):
        if self.image:
            return self.image.url
        else:
            return 'defaultimage'

    def __str__(self):
        return self.name
