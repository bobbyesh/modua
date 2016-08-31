from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^article/$', views.ArticleView.as_view(), name='article'),
]
