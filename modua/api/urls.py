from django.conf.urls import url, include
from . import views
from rest_framework.authtoken import views as authtoken_views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'user/definitions', views.UserDefinitionViewSet, base_name='user-definition')
router.register(r'user/words', views.UserWordViewSet, base_name='user-word')
router.register(r'definitions', views.PublicDefinitionViewSet, base_name='public-definition')
router.register(r'words', views.PublicWordViewSet, base_name='public-word')

urlpatterns = [
    # API Root
    url(r'^$', views.api_root, name='api-root'),
    url(r'^', include(router.urls)),
    url(r'^article/', views.PublicArticleView.as_view(), name='public-article'), # POST

    # Authentication views
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
]
