# landing/urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^signup/', views.SignupView.as_view(), name="signup"),
    url(r'^signup/success/', views.SignupSuccessView.as_view(), name="signup-success"),
    url(r'^signin/', views.SigninView.as_view(), name="signin"),
    url(r'^signin/complete/', views.SigninCompleteView.as_view(), name="signin-complete"),
    url(r'^annotate/', views.AnnotationView.as_view(), name="annotation"),
    url(r'^annotate_complete/', views.AnnotationCompleteView.as_view(), name="annotate-complete"),

]
