from skills.models import Project, Comment, Like

def fatfooter_data(request):
    recent_activity_count = 7

    recent_comments = Comment.objects.filter(is_deleted=False, project__is_deleted=False, project__trainingbit__is_draft=False).prefetch_related('author', 'project').order_by('-created_at')[:recent_activity_count]
    recent_likes    = Like.objects.all().prefetch_related('author', 'content_object').order_by('-created_at')[:recent_activity_count]

    recent_activity = list(recent_comments) + list(recent_likes)
    recent_activity.sort(key=lambda a: a.created_at, reverse=True)

    l = []
    for activity in recent_activity:
        if type(activity) == Like:
            l.append((activity.author, 'liked', activity.content_object))
        elif type(activity) == Comment:
            l.append((activity.author, 'commented on', activity.project))

    return {
        'recent_projects': Project.objects \
                            .filter(is_deleted=False, trainingbit__is_draft=False) \
                            .select_related('author__username') \
                            .select_related('author__image')    \
                            .order_by('-created_at')[:3],
        'recent_activity': l[:recent_activity_count]
    }

