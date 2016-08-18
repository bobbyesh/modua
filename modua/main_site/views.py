import unicodedata
from django.views.generic import View, ListView, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist

from .forms import RegistrationForm, AnnotationForm
from modua_app.models import Definitions, Languages

from wordfencer.parser import ChineseParser, is_cjk_punctuation
import pdb



def build_html(**kwargs):
    if 'tag' not in kwargs:
        raise Exception("Must contain kwarg `tag`.")
    if 'content' not in kwargs:
        raise Exception("Must contain kwarg `content`.")

    # You can't use python's keyword `class` as a kwarg, so use `cls` instead.
    # This code sets the 'class' kwarg to pass in for the html class attribute.
    if 'cls' in kwargs:
        kwargs['class'] = kwargs['cls']

    tag = kwargs.pop('tag')
    content = kwargs.pop('content')

    attributes = ''
    for key, val in kwargs.items():
        attributes += ' {}="{}" '.format(key, val)

    open_tag = '<{tag} {attributes}>'.format(tag=tag, attributes=attributes)
    closing_tag = '</{tag}>'.format(tag=tag)
    return "{open_tag} {content} {closing_tag}".format(
        open_tag=open_tag,
        content=content,
        closing_tag=closing_tag
    )


def build_popup_html(word, definition):
    header = build_html(tag='h3',content=word)
    div = build_html(tag='div', content=definition)
    outer_span =  build_html(content=header + div, tag='div', name=word, cls='popup')
    return outer_span


def build_word_html(word):
    return build_html(content=word, tag='span', name=word, cls='word')


class HomeView(TemplateView):
    template_name = 'main_site/home.html'

class RegistrationView(FormView):
    template_name = 'main_site/register.html'
    form_class = RegistrationForm
    success_url = '/home/success/'

    def form_valid(self, form):
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create(username=username,
                                email=email,
                                password=password)
        return super(RegistrationView, self).form_valid(form)

class RegistrationSuccessView(TemplateView):
    template_name = 'main_site/success.html'


class AnnotationView(FormView):
    template_name = 'main_site/annotation.html'
    form_class = AnnotationForm
    success_url = '/home/annotate_complete/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            text = form.cleaned_data['text']
            request.session['text'] = text
            parser = ChineseParser()
            words = parser.parse(text)
            popups = []
            for idx, word in enumerate(words):
                if len(word) > 1:
                    word_html = build_word_html(word)
                    words[idx] = word_html
                    definitions = self.get_definition_or_empty(word)
                    popups.append(build_popup_html(word, definitions))
                    # Any unicode category starting with a P is punctuation
                elif not unicodedata.category(word).startswith('P'):
                    word_html = build_word_html(word)
                    words[idx] = word_html
                    definitions = self.get_definition_or_empty(word)
                    popups.append(build_popup_html(word, definitions))

            request.session['words'] = words
            request.session['popups'] = popups
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def get_definition_or_empty(self, word):
        s = ''
        try:
            language = Languages.objects.get(language='zh')
            definitions = Definitions.objects.filter(word=word, language=language)
            for d in definitions:
                s += d.definition + ' / '
        except ObjectDoesNotExist:
            pass
        return s


class AnnotationCompleteView(TemplateView):
    template_name = 'main_site/annotate_complete.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['text'] = request.session['text']
        context['words'] = request.session['words']
        context['popups'] = request.session['popups']
        return self.render_to_response(context)


class LoginView(TemplateView):
    pass


class UserPageView(TemplateView):
    pass


class WordListView(ListView):
    pass


class WordDetailView(DetailView):
    pass

class AddDefinitionView(FormView):
    pass

