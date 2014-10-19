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
                 label='Draft status',
                 initial=True
             )

class SkillForm(ModelForm):
    is_draft = DraftField

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Name the skill'}),
        error_messages={'required': 'You must give a name to the skill'},
    )
    description = forms.CharField(
        widget=widgets.Textarea(attrs={'placeholder': 'Describe the skill'}),
        error_messages={'required': 'You must fill out a description'},
    )
    normal_flag_image = forms.ImageField(
        widget=widgets.ClearableFileInput(),
        required=False
    )
    completed_flag_image = forms.ImageField(
        widget=widgets.ClearableFileInput(),
        required=False
    )

    class Meta:
        model = Skill
        fields = ['name', 'description', 'is_draft', 'normal_flag_image', 'completed_flag_image']


class TrainingBitForm(ModelForm):
    is_draft = DraftField

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Name the training bit'}),
        error_messages={'required': 'You must give a name to the training bit'},
    )
    description = forms.CharField(
        widget=widgets.Textarea(attrs={'placeholder': 'Describe the training bit'}),
        error_messages={'required': 'You must fill out a description'},
    )

    class Meta:
        model = TrainingBit
        fields = ['name', 'description', 'label', 'is_draft', 'image']


class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'content', 'image', 'link_title', 'link_url', 'video']

    def clean(self, *args, **kwargs):
        data_list = [self.cleaned_data.get('link_title'), self.cleaned_data.get('link_url')]
        none_list = list(filter(lambda r: r == '', data_list))
        if len(none_list) == 1:
            raise forms.ValidationError("Your link must have both a title and a URL")

        return super(ProjectForm, self).clean(*args, **kwargs)


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['text', 'parent', 'project']


class TopicForm(ModelForm):

    class Meta:
        model = Topic
        fields = ['name']
