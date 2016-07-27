from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    url(r'^languages/(?P<language>[\w-]+)/(?P<word>[\w-]+)', views.DefinitionListView.as_view(), name='definition-word-list'),
    url(r'^languages/(?P<language>[\w-]+)/', views.DefinitionListView.as_view(), name='definition-list'),
    url(r'^languages/', views.LanguageListView.as_view(), name='language-list'),
    url(r'^$', views.api_root, name='api-root'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
