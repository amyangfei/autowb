from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'cron.views',

    url(r'^send/test$', 'send_test', {'template': 'sent.html'}, name='send_test'),

    url(r'^add$', 'cron_add', {'template': 'cron_add.html'}, name='cron_add'),
)
