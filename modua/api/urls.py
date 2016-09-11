from django.conf.urls import url, include
from . import views
from rest_framework.authtoken import views as authtoken_views


urlpatterns = [
    # API Root
    url(r'^$', views.api_root, name='api-root'),

    # Authentication views
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),

    # Public views
    url(r'^languages/$', views.LanguageListView.as_view(), name='language-list'),
    url(r'^languages/(?P<language>[\w-]+)/parse/$', views.ParseView.as_view(), name='parse'),
    url(r'^languages/(?P<language>[\w-]+)/words/$', views.PublicWordListView.as_view(), name='public-word-list'),
    url(r'^languages/(?P<language>[\w-]+)/definitions/(?P<word>[\w-]+)/$', views.PublicDefinitionListView.as_view(), name='public-definition-list'),

    # User-specific views
    url(r'^user/languages/(?P<language>[\w-]+)/(?P<word>[\w-]+)/$', views.UserWordDetailView.as_view(), name='user-word-detail'), # GET, POST, PATCH
    url(r'^user/languages/(?P<language>[\w-]+)/definitions/(?P<word>[\w-]+)/$', views.UserDefinitionListView.as_view(), name='user-definition-list'), # GET
    url(r'^user/languages/(?P<language>[\w-]+)/(?P<word>[\w-]+)/definitions/$', views.UserDefinitionCreateDestroyView.as_view(), name='user-definition-create-destroy'), # GET, POST, DELETE

    # TODO
    # r'^user/languages/(?P<language>[\w-]+)/definitions/$  # All of the user's definitions for this language
    # r'^user/languages/(?P<language>[\w-]+)/definitions/(?P<word>[\w-]+)/$ All of the user's definitions for this one word

    # Temporarily deprecated
    # url(r'^import/$', views.URLImportView.as_view(), name='url-import'),
]
