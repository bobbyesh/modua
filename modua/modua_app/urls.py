from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^user-auth/search/(?P<language>[\w-]+)/(?P<word>[\w-]+)', views.SearchByUserView.as_view(), name='search_by_user'),
    url(r'^search/(?P<language>[\w-]+)/(?P<word>[\w-]+)', views.SearchView.as_view(), name='search'),
    url(r'^languages/', views.LanguageListView.as_view(), name='language_list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
