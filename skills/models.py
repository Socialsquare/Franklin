from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.text import slugify


# Django forms
from django.forms import ValidationError

# Generic relations
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# Signals
from django.db.models.signals import post_save
from django.dispatch import receiver

# Email
from django.core.mail import send_mail

# Python modules
from datetime import datetime
import re

# Custom fields
from sortedm2m.fields import SortedManyToManyField
from embed_video.fields import EmbedVideoField


# South (fix)
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


# Please have this model as a parent for your models if you want the model to
# use slugs in its URL.
class SluggedModel(models.Model):
    # Relations
    slug = models.SlugField(max_length=60, db_index=True, null=False, blank=False, unique=True)

    class Meta:
        abstract = True

    # From: http://stackoverflow.com/a/837835/118608
    def save(self, *args, **kwargs):
        if not self.pk:
            # The object has "just" been created (not in the database yet)
            # so set the slug
            slug = slugify(self.name)

            if self.__class__.objects.filter(slug__exact=slug).exists():
                # An object with this slug already exists!
                existing_slugs = self.__class__.objects.\
                                     filter(slug__regex='^' + slug + r'-\d+').\
                                     values_list('slug', flat=True)
                if len(existing_slugs) > 0:
                    # Grab number from highest existing slug
                    last_existing_slug = sorted(existing_slugs)[-1]
                    m = re.match(r'^.*-(\d+)$', last_existing_slug)
                    id_counter = int(m.group(1)) + 1
                else:
                    id_counter = 1

                # Generate new unique slug
                slug = '%s-%u' % (slug, id_counter)

            self.slug = slug

        super(SluggedModel, self).save(*args, **kwargs)


#### CONCRETE MODELS

class Like(TimedModel, AuthoredModel):
    # https://docs.djangoproject.com/en/1.6/ref/contrib/contenttypes/#id1
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    # http://timmyomahony.com/blog/reversing-unique-generic-foreign-key-django/
    def validate_unique(self, *args, **kwargs):
        super(Like, self).validate_unique(*args, **kwargs)

        if self.__class__.objects.filter(author=self.author,
                                         content_type=self.content_type,
                                         object_id=self.object_id).exists():
            raise ValidationError({
                'NON_FIELD_ERRORS': ('You already liked this',)
            })


class Image(TimedModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='uploaded_images', blank=False)
    image = models.ImageField(upload_to='trainingbits', blank=True)
    identifier = models.CharField(max_length=36)


class TrainingBit(TimedModel, AuthoredModel, SluggedModel):
    LABELS = (
        ('I', 'Inspiration'),
        ('B', 'Background'),
        ('T', 'Tool'),
    )

    # Content
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='trainingbits', blank=True)
    label = models.CharField(max_length=1, choices=LABELS, blank=False)
    json_content = models.TextField(default='{"learn":[],"act":[],"share":[]}')

    # Relations
    likes = generic.GenericRelation(Like)

    # Flags
    recommended = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)

    def getImage(self):
        if self.image and self.image.url != '':
            return self.image.url
        else:
            return '/static/images/trainingbit-cover-placeholder.png'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('skills:trainingbit_cover', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-created_at']


class Project(TimedModel, AuthoredModel, SluggedModel):

    # Content
    name = models.CharField(max_length=100, blank=False)
    content = models.TextField(blank=False)
    image = models.ImageField(upload_to='trainingbits', blank=True)
    link_title = models.CharField(max_length=100, blank=True)
    link_url = models.URLField(blank=True)
    video = EmbedVideoField(blank=True, null=True)

    # Relations
    trainingbit = models.ForeignKey(TrainingBit, blank=False)
    likes = generic.GenericRelation(Like)

    # Flags
    is_public = models.BooleanField(default=True)
    is_flagged = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    # def getImage(self):
    #     if self.image:
    #         return self.image.url
    #     else:
    #         return ''

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return reverse('skills:trainingbit_view', args=[self.trainingbit.id]) + \
        #        '#project-%u' % self.id
        return reverse('skills:project_view', kwargs={'slug': self.slug})

    def root_comments(self):
        return self.comment_set.filter(parent=None)


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

    # only allow threading to one level
    def allow_thread(self):
        return self.parent is None

    def get_absolute_url(self):
        return self.project.get_absolute_url() + ('#comment-%u' % self.pk)


class Skill(TimedModel, AuthoredModel, SluggedModel):

    # Content
    name = models.CharField(max_length=30)
    description = models.TextField()

    # Relations
    #   optional relation to training bits (i.e. a skill does _have_ to have a
    #   training bit)
    trainingbits = SortedManyToManyField(TrainingBit, blank=True)
    likes = generic.GenericRelation(Like)

    # Flags
    is_draft = models.BooleanField(default=True)

    def trainingbit_count(self):
        return self.trainingbits.filter(is_draft=False).count()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('skills:skill_view', kwargs={'slug': self.slug})


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


#### PERMISSIONS

# apply AuthorPermissionLogic and CollaboratorsPermissionLogic
from permission import add_permission_logic
from permission.logics import PermissionLogic, AuthorPermissionLogic
# from permission.logics import CollaboratorsPermissionLogic

# Authors have full permission (edit, delete etc.) to their own skills and training bits
gcl_authorpermissionlogic = AuthorPermissionLogic(
    field_name='author',
    change_permission=True,
    delete_permission=True
)
add_permission_logic(Skill, gcl_authorpermissionlogic)
add_permission_logic(TrainingBit, gcl_authorpermissionlogic)
add_permission_logic(Project, gcl_authorpermissionlogic)
add_permission_logic(Comment, gcl_authorpermissionlogic)

# See: https://github.com/lambdalisue/django-permission/blob/bdd0ebefbb6638b38886a0d35d9d379cfb067bfd/src/permission/logics/author.py


class AdminPermissionLogic(PermissionLogic):
    def has_perm(user, permission_str, obj):
        if user.is_admin:
            return True
        else:
            return False

# Admin always have full permission
add_permission_logic(Skill, AdminPermissionLogic())
add_permission_logic(TrainingBit, AdminPermissionLogic())
add_permission_logic(Comment, AdminPermissionLogic())


#### SIGNALS

@receiver(post_save, sender=Comment)
def send_notification_email(sender, **kwargs):
    if kwargs['created']:
        comment = kwargs['instance']

        is_reply = comment.parent is not None
        author_has_email = comment.author.email is not None and comment.author.email != ''
        if is_reply and author_has_email:
            print('Sending mail to: %s <%s>' % (comment.parent.author.username,  comment.parent.author.email))

            # From: http://stackoverflow.com/a/8817935/118608
            from django.contrib.sites.models import get_current_site
            request = None
            full_url = ''.join(['http://', get_current_site(request).domain, comment.get_absolute_url()])
            #'Click here to see the comment %s' % full_url,

            email_subject = 'You got a reply on your comment on Global Change Lab'
            email_body = '%s just commented on your comment on %s!\r\n\r\n%s' % (comment.author.username, comment.project.name, full_url)
            email_from = 'Global Change Lab <hello@globalchangelab.org>'
            email_to = [comment.parent.author.email]

            send_mail(email_subject,
                      email_body,
                      email_from,
                      email_to,
                      fail_silently=False)
