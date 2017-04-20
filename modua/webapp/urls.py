from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^article/(?P<pk>[0-9]+)/$', views.ArticleView.as_view(), name='article'),
    url(r'^account/$', views.AccountView.as_view(), name='account'),
    url(r'^change_username/$', views.ChangeUsernameView.as_view(), name='change_username'),
    url(r'^change_password/$', views.ChangePasswordView.as_view(), name='change_password'),
    url(r'^delete_account/$', views.DeleteAccountView.as_view(), name='delete_account'),
    url(r'^delete_account_redirect/$', views.DeleteAccountRedirectView.as_view(), name='delete_account_redirect'),
    url(r'^user_stats/$', views.UserStatsView.as_view(), name='user_stats'),
]
