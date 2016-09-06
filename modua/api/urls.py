from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.api_root, name='api-root'),
    url(r'^languages/$', views.LanguageListView.as_view(), name='language-list'),
    url(r'^languages/(?P<language>[\w-]+)/word/(?P<word>[\w-]+)/$', views.WordDetailView.as_view(), name='word-detail'),
    url(r'^languages/(?P<language>[\w-]+)/word/(?P<word>[\w-]+)/definitions/$', views.DefinitionListView.as_view(), name='definition-list'),
    url(r'^languages/(?P<language>[\w-]+)/parse/$', views.ParseView.as_view(), name='parse'),
    url(r'^import/$', views.URLImportView.as_view(), name='url-import'),
]
