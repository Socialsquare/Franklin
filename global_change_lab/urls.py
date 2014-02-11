from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'global_change_lab.views.front_page', name='front_page'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^skills/', include('skills.urls', namespace='skills')),

    url(r'^shares$', 'global_change_lab.views.shares', name='shares'),

    # django-allauth
    # url(r'^user/', include('allauth.urls', namespace='allauth', app_name='user')),
    url(r'^user/dashboard', 'global_change_lab.views.trainer_dashboard', name='trainer_dashboard'),
    url(r'^user/', include('allauth.urls')),
    url(r'^user/profile/(\d+)?', 'global_change_lab.views.profile', name='profile'),

    # django-comments-xtd
    url(r'^comments/', include('django_comments_xtd.urls')),

    # url(r'^/', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

from django.conf import settings

if settings.LOCALHOST:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
