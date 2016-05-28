from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [

    url(r'^$', views.Home.as_view(), name="home"),
    url(r'^$', views.Login.as_view(), name ="login"),
    url(r'^$', views.UserPage.as_view(), name="user_page"),
    url(r'^$', views.WordList.as_view(), name="word_list"),
    url(r'^$', views.WordDetail(), name="word_detail"),

]
