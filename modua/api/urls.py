from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    url(r'^$', views.api_root, name='api-root'),
    url(r'^languages/(?P<language>[\w-]+)/(?P<word>[\w-]+)/(?P<id>[0-9]+)/$', views.DefinitionDetailView.as_view(),
                                name='definition-detail'),
    url(r'^languages/(?P<language>[\w-]+)/(?P<word>[\w-]+)/$', views.DefinitionListView.as_view(),
                                name='definition-list'),
    url(r'^languages/$', views.LanguageListView.as_view(), name='language-list'),
    url(r'^languages/(?P<language>[\w-]+)/$', views.DefinitionListView.as_view(), name='language-definitions'),
    url(r'^languages/(?P<language>[\w-]+)/sentence/', views.SentenceView.as_view(), name='sentence'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
