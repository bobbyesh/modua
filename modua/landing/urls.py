# landing/urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^signup/', views.SignupView.as_view(), name="signup"),
    url(r'^signup/success/', views.SignupSuccessView.as_view(), name="signup-success"),
    url(r'^login/$', views.SigninView.as_view(), name="login"),
    url(r'^contact/', views.ContactView.as_view(), name="contact"),
    url(r'^about/', views.AboutView.as_view(), name="about"),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^delete_account_success/$', views.DeleteAccountSuccessView.as_view(), name='delete_account_success'),
]
