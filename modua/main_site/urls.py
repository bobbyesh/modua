from django.conf.urls import url
from . import views

urlpatterns = [
    # TODO regex to match word
    url(r'^$', views.HomeView.as_view(), name="home"),
]
