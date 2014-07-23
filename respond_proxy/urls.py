from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^respond\.proxy\.js$', 'respond_proxy.views.respond_proxy_js'),
    url(r'^respond\.proxy\.gif$', 'respond_proxy.views.respond_proxy_gif'),
)