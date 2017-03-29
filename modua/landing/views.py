import unicodedata
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from wordfencer.parser import ChineseParser


from .forms import SignupForm, AnnotationForm, SigninForm
from api.models import PublicDefinition
from core.utils import build_popup_html, build_word_html


class IndexView(TemplateView):
    template_name = 'landing/index.html'


class ContactView(TemplateView):
    template_name = 'landing/contact.html'


class AboutView(TemplateView):
    template_name = 'landing/about.html'


class SigninView(FormView):
    model = User
    template_name = 'landing/signin.html'
    form_class = SigninForm

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect('webapp:home')
        else:
            '''

            .. TODO: Create reasonable invalid user redirection.

            '''
            return redirect('signin')


class SignupView(CreateView):
    model = User
    template_name = 'landing/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('webapp:home')

    def form_valid(self, form):
        valid = super(SignupView, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        email = form.cleaned_data.get('email')
        title = 'Sign Up Confirmation at Readable!'
        body = 'Thanks for signing up at Readable!'
        email = EmailMessage(title, body, to=[email])
        email.send()
        return valid

class SignupSuccessView(TemplateView):
    template_name = 'landing/success.html'


class AnnotationView(FormView):
    template_name = 'landing/annotation.html'
    form_class = AnnotationForm
    success_url = reverse_lazy('annotate-complete')

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
            definitions = PublicDefinition.objects.filter(word=word)
            unique_definitions = list(set([x.definition for x in definitions]))
            for definition in unique_definitions:
                s += definition + ' / '
        except ObjectDoesNotExist:
            pass
        return s


class AnnotationCompleteView(TemplateView):
    template_name = 'landing/annotate_complete.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['text'] = request.session['text']
        context['words'] = request.session['words']
        context['popups'] = request.session['popups']
        return self.render_to_response(context)
