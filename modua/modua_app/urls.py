from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/search/(?P<language_tag>[\w-]+)/(?P<language_tag>[\w-]+)', views.Search.as_view(), name='search'),
]
