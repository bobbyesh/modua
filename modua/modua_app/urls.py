from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^search/(?P<language>[\w-]+)/(?P<word>[\w-]+)', views.SearchView.as_view(), name='search'),
]
