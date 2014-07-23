from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # global-change-lab
    #   front-page and welcome
    url(r'^$', 'global_change_lab.views.front_page', name='front_page'),
    url(r'^welcome/?$', 'global_change_lab.views.new_user', name='new_user'),
    url(r'^welcome/info/?$', 'global_change_lab.views.new_user_input_details', name='new_user_input_details'),
    url(r'^welcome/topics/?$', 'global_change_lab.views.new_user_topics', name='new_user_topics'),
    url(r'^welcome/suggestions/?$', 'global_change_lab.views.new_user_suggestions', name='new_user_suggestions'),
    #   users
    url(r'^user/list/?$', 'global_change_lab.views.user_list', name='user_list'),
    url(r'^user/profile/(\d+)?$', 'global_change_lab.views.profile', name='profile'),
    url(r'^user/profile/upload/?$', 'global_change_lab.views.upload_profile_picture', name='upload_profile_picture'),
    url(r'^user/delete/(\d+)/?$', 'global_change_lab.views.user_delete', name='user_delete'),
    url(r'^user/make_trainer/(\d+)/?$', 'global_change_lab.views.user_upgrade_to_trainer', name='user_upgrade_to_trainer'),
    #   trainers
    url(r'^trainer/dashboard/?$', 'global_change_lab.views.trainer_dashboard', name='trainer_dashboard'),
    url(r'^trainer/dashboard/statistics/?$', 'global_change_lab.views.statistics', name='statistics'),
    #   admins
    url(r'^admin/dashboard/?$', 'global_change_lab.views.admin_dashboard', name='admin_dashboard'),
    url(r'^admin/flagged-comments/?$', 'global_change_lab.views.admin_flagged_comments', name='admin_flagged_comments'),
    url(r'^admin/flagged-shares/?$', 'global_change_lab.views.admin_flagged_shares', name='admin_flagged_shares'),
    url(r'^admin/users.csv$', 'global_change_lab.views.admin_users_csv', name='admin_users_csv'),
    url(r'^admin/statistics.csv$', 'global_change_lab.views.admin_statistics_csv', name='admin_statistics_csv'),
    #   flatpages
    url(r'^page/new/?$', 'global_change_lab.views.page_new', name='page_new'),
    url(r'^page/edit/(\d+)/?$', 'global_change_lab.views.page_edit', name='page_edit'),
    url(r'^page/delete/(\d+)/?$', 'global_change_lab.views.page_delete', name='page_delete'),
    # Picture upload URL
    url(r'^picture/upload/?$', 'global_change_lab.views.upload_picture', name="upload_picture"),

    # skills
    url(r'^', include('skills.urls', namespace='skills')),

    # django-allauth
    # url(r'^user/', include('allauth.urls', namespace='allauth', app_name='user')),
    url(r'^user/', include('allauth.urls')),

    # django.contrib.admin
    url(r'^admin/', include(admin.site.urls)),

    # django.contrib.flatpages
    url(r'^pages', include('django.contrib.flatpages.urls')),
    # In reality this creates URLs like this:
    #   r'^pages<page.url>'
    # but flatpages enforce `page.url` to have leading and trailing slashes
    # therefore the flatpages base URL _must not_ have a trailing slash!

    # respond-proxy
    url(r'^', include('respond_proxy.urls', namespace='respond_proxy')),
)

urlpatterns += staticfiles_urlpatterns()

from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

if settings.DEBUG:
    style_view = lambda r: render(r, 'debug_styles.html')

    from django.shortcuts import render

    urlpatterns += patterns('',
        url(r'^debug_styles/?$', style_view, name='debug_styles'),
    )

# django.contrib.flatpages
urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^terms/$', 'flatpage', {'url': '/terms-of-service/'}, name='terms'),
    url(r'^creative-commons/$', 'flatpage', {'url': '/creative-commons/'}, name='creative-commons'),
)

# django-inlinetrans
urlpatterns += patterns('',
    url(r'^inlinetrans/', include('inlinetrans.urls')),
)
