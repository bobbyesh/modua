from django.conf.urls import url
from . import views
from rest_framework.authtoken import views as authtoken_views


urlpatterns = [
    url(r'^$', views.api_root, name='api-root'),
    url(r'^languages/$', views.LanguageListView.as_view(), name='language-list'),
    url(r'^languages/(?P<language>[\w-]+)/word/(?P<word>[\w-]+)/$', views.WordDetailView.as_view(), name='word-detail'),
    url(r'^languages/(?P<language>[\w-]+)/create_word/(?P<word>[\w-]+)/$', views.WordCreateView.as_view(), name='word-create'),
    # Implement word CreateAPIView, perhaps singular instead of plural
    url(r'^languages/(?P<language>[\w-]+)/definitions/(?P<word>[\w-]+)/$', views.DefinitionListView.as_view(), name='definition-list'),
    # Implement definition CreateAPIView, perhaps singular instead of plural
    url(r'^import/$', views.URLImportView.as_view(), name='url-import'),
    url(r'^languages/(?P<language>[\w-]+)/word/(?P<word>[\w-]+)/definitions/(?P<definition>[\w-]+)/$', views.DefinitionDetailView.as_view(), name='definition-detail'),
    url(r'^api-token-auth/', authtoken_views.obtain_auth_token),

    # Public views
    url(r'^languages/(?P<language>[\w-]+)/parse/$', views.ParseView.as_view(), name='parse'),

    # User-specific views
    url(r'^user/languages/(?P<language>[\w-]+)/(?P<word>[\w-]+)/$', views.UserWordDetailView.as_view(), name='user-word-detail'),

    # TODO
    # r'^user/languages/(?P<language>[\w-]+)/definitions/$  All of the user's definitions
    # r'^user/languages/(?P<language>[\w-]+)/definitions/(?P<word>[\w-]+)/$ All of the user's definitions for this one word
]
