from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',

    (r'^favicon\.ico$', RedirectView.as_view(url='/media/favicon.ico')),
    (r'^media/(?P<path>.+)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    url(r'^$', 'views.index', {'template': 'index.html'}, name='index'),
    url(r'^home$', 'views.home', {'template': 'home.html'}, name='home'),

    # account
    url(r'^account/', include('account.urls')),

    # social auth
    url(r'social/', include('social_auth.urls')),

    # weibo cron
    url(r'cron/', include('cron.urls')),
)
