from skills.models import Project
from skills.models import Comment

def fatfooter_data(request):
    return {
        'recent_projects': Project.objects.all()                 \
                            .select_related('author__username') \
                            .select_related('author__image')    \
                            .order_by('-created_at')[:3],
        'recent_comments': Comment.objects.all().order_by('-created_at')[:5]
    }

