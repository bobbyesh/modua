from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^article/(?P<slug>[\w-]+)/$', views.ArticleView.as_view(), name='article'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^logout/success/$', views.LogoutSuccessView.as_view(), name='logout_success'),
]
