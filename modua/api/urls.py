from django.conf.urls import url, include
from . import views
from rest_framework.authtoken import views as authtoken_views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'user/definitions', views.UserDefinitionViewSet, base_name='user-definition')

urlpatterns = [
    # API Root
    url(r'^$', views.api_root, name='api-root'),

    # Authentication views
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),

    # Public views
    url(r'^parse/$', views.ParseView.as_view(), name='parse'),
    url(r'^words/$', views.PublicWordListView.as_view(), name='public-word-list'),
    url(r'^definitions/(?P<word>[\w-]+)/$', views.PublicDefinitionListView.as_view(), name='public-definition-list'),
    url(r'^article/$', views.PublicArticleView.as_view(), name='public-article'), # POST

    # User-specific views
    url(r'^user/(?P<word>[\w-]+)/$', views.UserWordDetailView.as_view(), name='user-word-detail'), # GET, POST, PATCH
] + router.urls
