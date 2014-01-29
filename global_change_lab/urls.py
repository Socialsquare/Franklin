from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'global_change_lab.views.front_page', name='front_page'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^skills/', include('skills.urls')),

    # url(r'^/', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
