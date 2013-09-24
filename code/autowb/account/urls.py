from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'account.views',
    url(r'^test$', 'test', {'template': 'test.html'}, name="test"),
    url(r'^login$', 'login', {'template': 'login.html'}, name="login"),
    url(r'^logout$', 'logout', name="logout"),
    url(r'^user_settings$', 'user_settings', {'template': 'user_settings.html'}, name='user_settings'),
    url(r'^signup/done$', 'signup_done', {'template': 'signup_done.html'}, name="signup_done"),
)
