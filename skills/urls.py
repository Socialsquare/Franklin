from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'skills.views.skills_overview', name="skills_overview"),
    url(r'^(\d+)$', 'skills.views.skill_view', name='skill_view'),
    url(r'^trainingbits$', 'skills.views.trainingbits_overview', name="trainingbits_overview"),

    url(r'^trainingbit/new$', 'skills.views.trainingbit_edit', name='trainingbit_new'),
    url(r'^trainingbit/(\d+)/edit$', 'skills.views.trainingbit_edit', name="trainingbit_edit"),
    url(r'^trainingbit/(\d+)/edit-content$', 'skills.views.trainingbit_edit_content', name="trainingbit_edit_content"),
    url(r'^trainingbit/(\d+)/view$', 'skills.views.trainingbit_view', name="trainingbit_view"),
    url(r'^trainingbit/(\d+)/delete$', 'skills.views.trainingbit_delete', name="trainingbit_delete"),
    url(r'^trainingbit/(\d+)/recommend$', 'skills.views.trainingbit_recommend', name="trainingbit_recommend"),

    # TODO: These are stubs, and must be implemented
    url(r'^skill/new$', 'skills.views.skill_edit', name='skill_new'),
    url(r'^skill/(\d+)/edit$', 'skills.views.skill_edit', name="skill_edit"),
    # url(r'^admin/', include(admin.site.urls)),
)
