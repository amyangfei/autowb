from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'cron.views',

    url(r'^send/test$', 'send_test', {'template': 'send_test.html'}, name='send_test'),

    url(r'^add$', 'cron_add', {'template': 'cron_add.html'}, name='cron_add'),
    url(r'^delete/(?P<wbcnt_id>[\w.@+-]+)$', 'cron_delete', name='cron_delete'),
    url(r'^unsent/list$', 'cron_unsent_list', {'template': 'unsent_list.html'}, name='cron_unsent_list'),
    url(r'^sunsent/list$', 'cron_s_unsent_list', {'template': 's_unsent_list.html'}, name='cron_s_unsent_list'),
)
