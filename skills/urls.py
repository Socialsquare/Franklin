from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Training Bit URLs
    url(r'^trainingbits/([-\w]+)/?$', 'skills.views.trainingbits_overview', name="trainingbits_overview"),
    url(r'^trainingbits$', 'skills.views.trainingbits_overview', name="trainingbits_overview"),
    url(r'^trainingbit/new$', 'skills.views.trainingbit_edit', name='trainingbit_new'),
    url(r'^trainingbit/(\d+)/edit$', 'skills.views.trainingbit_edit', name="trainingbit_edit"),
    url(r'^trainingbit/(\d+)/edit-content$', 'skills.views.trainingbit_edit_content', name="trainingbit_edit_content"),
    url(r'^trainingbit/(\d+)/cover$', 'skills.views.trainingbit_cover', name="trainingbit_cover"),
    url(r'^trainingbit/(\d+)/view$', 'skills.views.trainingbit_view', name="trainingbit_view"),
    url(r'^trainingbit/(\d+)/delete$', 'skills.views.trainingbit_delete', name="trainingbit_delete"),
    url(r'^trainingbit/(\d+)/recommend$', 'skills.views.trainingbit_recommend', name="trainingbit_recommend"),
    url(r'^trainingbit/(\d+)/start$', 'skills.views.trainingbit_start', name="trainingbit_start"),
    url(r'^trainingbit/(\d+)/stop$', 'skills.views.trainingbit_stop', name="trainingbit_stop"),

    # Skill URLs
    url(r'^skills/$', 'skills.views.skills_overview', name="skills_overview"),
    url(r'^skills/drafts/?$', 'skills.views.skills_overview', {'show_drafts':True}, name="skills_overview_all"),
    url(r'^skills/([-\w]+)/?$', 'skills.views.skills_overview', name="skills_overview"),
    url(r'^skills/([-\w]+)/drafts/?$', 'skills.views.skills_overview', {'show_drafts':True}, name="skills_overview_all"),
    url(r'^skill/(\d+)$', 'skills.views.skill_view', name='skill_view'),
    url(r'^skill/new$', 'skills.views.skill_edit', name='skill_new'),
    url(r'^skill/(\d+)/edit$', 'skills.views.skill_edit', name="skill_edit"),
    url(r'^skill/(\d+)/publicize$', 'skills.views.skill_publicize', name="skill_publicize"),
    url(r'^skill/(\d+)/delete$', 'skills.views.skill_delete', name="skill_delete"),
    url(r'^skill/(\d+)/start$', 'skills.views.skill_start', name="skill_start"),
    url(r'^skill/(\d+)/stop$', 'skills.views.skill_stop', name="skill_stop"),
    url(r'^skill/(\d+)/trainingbits.json$', 'skills.views.skill_trainingbits_json', name="skill_trainingbits_json"),

    # Project URLs
    url(r'^share/(\d+)/view$', 'skills.views.project_view', name="project_view"),

    # Like URLs
    url(r'^like/?$', 'skills.views.like', name="like"),

    # Topic URLs
    url(r'^topic/new/?$', 'skills.views.topic_new', name='topic_new'),
    url(r'^topic/delete/(\d+)/?$', 'skills.views.topic_delete', name='topic_delete'),

    # Comment URLs (projects, comments)
    url(r'^comment/post/?$', 'skills.views.comment_post', name="comment_post"),
    url(r'^comment/delete/(\d+)/?$', 'skills.views.comment_delete', name="comment_delete"),

    # Share URLs (projects, comments)
    url(r'^shares/?$', 'skills.views.shares_overview', name="shares_overview"),
)
