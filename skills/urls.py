from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'skills.views.skills_overview', name="skills_overview"),
    url(r'^(\d+)$', 'skills.views.skill', name='skill'),
    url(r'^trainingbits$', 'skills.views.trainingbits_overview', name="trainingbits_overview"),

    # TODO: These are stubs, and must be implemented
    url(r'^skill/new$', 'skills.views.skill', name='skill_new'),
    url(r'^trainingbit/new$', 'skills.views.trainingbit_new', name='trainingbit_new'),
    # url(r'^admin/', include(admin.site.urls)),
)
