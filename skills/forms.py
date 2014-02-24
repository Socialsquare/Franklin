from django.forms import ModelForm
from skills.models import Project


class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ['title', 'content', 'image']
