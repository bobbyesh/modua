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
from modua_app.utils import build_html, build_popup_html, build_word_html

from wordfencer.parser import ChineseParser
import pdb


'''

..TODO:  Move build_html, build_popup_html, build_word_html into utils module, or start a core app (a la Two Scoops of Django)?

'''


class IndexView(TemplateView):
    template_name = 'main_site/index.html'


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
                    definitions = self.get_definitions_or_empty(word)
                    popups.append(build_popup_html(word, definitions))
                    # Any unicode category starting with a P is punctuation
                elif not unicodedata.category(word).startswith('P'):
                    word_html = build_word_html(word)
                    words[idx] = word_html
                    definitions = self.get_definitions_or_empty(word)
                    popups.append(build_popup_html(word, definitions))

            request.session['words'] = words
            request.session['popups'] = popups
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def get_definitions_or_empty(self, word):
        s = ''
        try:
            language = Languages.objects.get(language='zh')
            definitions = Definitions.objects.filter(word=word, language=language)
            unique_definitions = list(set([x.definition for x in definitions]))
            for definition in unique_definitions:
                s += definition + ' / '
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
