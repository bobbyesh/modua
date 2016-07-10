from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name="home"),
    url(r'^registration/', views.RegistrationView.as_view(), name="registration"),
]
