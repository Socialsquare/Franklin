from django.forms import ModelForm
from skills.models import Like, Skill, TrainingBit, Project, Comment, Topic


class LikeForm(ModelForm):
    # def __init__(self, author, *args, **kwargs):
    #     self.author = author

    #     super(LikeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Like
        fields = ['content_type', 'object_id']


class SkillForm(ModelForm):

    class Meta:
        model = Skill
        fields = ['name', 'description', 'is_public']


class TrainingBitForm(ModelForm):

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
