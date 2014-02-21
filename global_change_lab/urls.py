from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'global_change_lab.views.front_page', name='front_page'),
    url(r'^first/?$', 'global_change_lab.views.new_user', name='new_user'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('skills.urls', namespace='skills')),

    url(r'^shares$', 'global_change_lab.views.shares', name='shares'),

    # django-allauth
    # url(r'^user/', include('allauth.urls', namespace='allauth', app_name='user')),
    url(r'^user/', include('allauth.urls')),

    # global-change-lab
    url(r'^user/list/?$', 'global_change_lab.views.user_list', name='user_list'),
    url(r'^user/me/?$', 'global_change_lab.views.user_progress', name='user_progress'),
    url(r'^user/profile/(\d+)?', 'global_change_lab.views.profile', name='profile'),
    url(r'^user/dashboard/?$', 'global_change_lab.views.trainer_dashboard', name='trainer_dashboard'),
    url(r'^user/dashboard/trainingbit_statistics/?$', 'global_change_lab.views.trainingbit_statistics', name='trainingbit_statistics'),
    url(r'^user/dashboard/skill_statistics/?$', 'global_change_lab.views.skill_statistics', name='skill_statistics'),
    url(r'^admin/dashboard/?$', 'global_change_lab.views.admin_dashboard', name='admin_dashboard'),
    url(r'^admin/users.csv$', 'global_change_lab.views.admin_users_csv', name='admin_users_csv'),
    url(r'^admin/statistics.csv$', 'global_change_lab.views.admin_statistics_csv', name='admin_statistics_csv'),
    url(r'^user/delete/(\d+)/?$', 'global_change_lab.views.user_delete', name='user_delete'),
    url(r'^user/make_trainer/(\d+)/?$', 'global_change_lab.views.user_upgrade_to_trainer', name='user_upgrade_to_trainer'),

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
