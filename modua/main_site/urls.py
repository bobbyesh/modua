from django.conf.urls import url
from . import views

urlpatterns = [
    # TODO regex to match word
    url(r'^$', views.HomeView.as_view(), name="home"),
'''
    url(r'^login/$', views.LoginView.as_view(), name="login"),

    # TODO regex to match usernames, i.e., user/{username}
    url(r'^user/(regex_for_username)$', views.UserPageView.as_view(), name="user_page"),

    # The tail end of this needs to be a key-value pair indicating which
    # language the word list is for
    #
    # There is no '$' at the end of this URL pattern, so any key-value pairs
    # that follow will be passed to the view.
    url(r'^user/word-list/', views.WordListView.as_view(), name="word_list"),

    # TODO regex to match username and word, i.e., user/{username}/word/{word}
    # The tail end of this will have to have key value pairs indicating which
    # word and which language.
    url(r'^user/(username_regex_)/word/', views.WordDetailView(), name="word_detail"),


    # TODO regex to match username, i.e., user/{username}/add-definition
    # There will need to have a key value pair indicating which word a definition
    # is being added for.
    #
    # There is no '$' at the end of this URL pattern, so any key-value pairs
    # that follow will be passed to the view.
    url(r'^user/(username_regex_)/word/add-definition/', views.AddDefinitionView().as_view(), name="add_definition"),
'''
]
