from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^article/(?P<slug>[\w-]+)/$', views.ArticleView.as_view(), name='article'),
    url(r'^account/$', views.AccountView.as_view(), name='account'),
    url(r'^change_username/$', views.ChangeUsernameView.as_view(), name='change_username'),
    url(r'^change_password/$', views.ChangePasswordView.as_view(), name='change_password'),
]
