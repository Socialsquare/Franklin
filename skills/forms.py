from django.forms import ModelForm
from skills.models import Project, Topic


class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ['title', 'content', 'image']


class TopicForm(ModelForm):

    class Meta:
        model = Topic
        fields = ['name']
