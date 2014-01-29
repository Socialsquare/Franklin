from django.db import models

LABELS = (
    ('inspiration', 'Inspiration'),
    ('background', 'Background'),
    ('doing', 'Doing'),
)


# Create your models here.
class TrainingBit(models.Model):
    name = models.CharField(max_length=30)
    minute_duration = models.IntegerField()
    label = models.CharField(max_length=16, choices=LABELS)

    image = models.ImageField(upload_to='trainingbits', default='defaultimage')

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=30)
    # optional relation to training bits (i.e. a skill does _have_ to have a
    # training bit)
    training_bits = models.ManyToManyField(TrainingBit, blank=True, null=True)

    def __str__(self):
        return self.name
