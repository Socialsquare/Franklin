from django import forms
from django.forms import ModelForm
from django.forms import widgets
from skills.models import Like, Skill, TrainingBit, Project, Comment, Topic


class LikeForm(ModelForm):
    # def __init__(self, author, *args, **kwargs):
    #     self.author = author

    #     super(LikeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Like
        fields = ['content_type', 'object_id']

# http://stackoverflow.com/a/854764/118608
DraftField = forms.TypedChoiceField(
                 coerce=lambda x: x == 'True',
                 choices=((False, 'Public'), (True, 'Draft')),
                 widget=forms.RadioSelect(),
                 required=True,
                 label='Draft status'
             )

class SkillForm(ModelForm):
    is_draft = DraftField


    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Name the skill'}))
    description = forms.CharField(widget=widgets.Textarea(attrs={'placeholder': 'Describe the skill'}))

    class Meta:
        model = Skill
        fields = ['name', 'description', 'is_draft']


class TrainingBitForm(ModelForm):
    is_draft = DraftField

    class Meta:
        model = TrainingBit
        fields = ['name', 'description', 'label', 'is_draft', 'image']


class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'content', 'image', 'link', 'video']


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['text', 'parent', 'project']


class TopicForm(ModelForm):

    class Meta:
        model = Topic
        fields = ['name']
