from django.forms import ModelForm
from skills.models import Project, Comment, Topic


class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'content', 'image']


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['text', 'parent', 'project']


class TopicForm(ModelForm):

    class Meta:
        model = Topic
        fields = ['name']
