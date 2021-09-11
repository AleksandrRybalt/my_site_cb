from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormView
from datetime import date as dt
from .forms import *
from .utils import DataMixin, rate_now


class Posts(DataMixin, ListView):
    model = models.PostsModel
    template_name = 'core/posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return self.model.objects.filter(is_published=True)


class AddPost(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'core/add_post.html'
    success_url = reverse_lazy('posts')


class Post(DataMixin, DetailView):
    model = models.PostsModel
    template_name = 'core/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'


class Category(DataMixin, ListView):
    model = models.PostsModel
    template_name = 'core/posts.html'
    slug_url_kwarg = 'category_slug'
    context_object_name = 'posts'

    def get_queryset(self):
        return self.model.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True)


class RegisterUser(DataMixin, CreateView):
    form_class = AddUserForm
    template_name = 'core/registr.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'core/authorization.html'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


class RateView(DataMixin, FormView):
    form_class = RateForm
    template_name = 'core/rate.html'
    success_url = reverse_lazy('rate')

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = self.form_class
        return self.get_context_rate(request, context)


class BikView(DataMixin, FormView):
    form_class = BikForm
    template_name = 'core/bik.html'
    success_url = reverse_lazy('bik')

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = self.form_class
        return self.get_context_bik(request, context)


class CurrencyDynamic(DataMixin, FormView):
    form_class = CurrencyDynamicForm
    template_name = 'core/currency_dynamic.html'
    success_url = reverse_lazy('currency_dynamic')

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = self.form_class
        return self.get_context_currency_dynamic(request, context)


class PreciousMetals(DataMixin, FormView):
    form_class = PreciousMetalsForm
    template_name = 'core/precious_metals.html'
    success_url = reverse_lazy('precious_metals')

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = self.form_class
        return self.get_context_precious_metals(request, context)


def about_us(request):
    data = {}
    rate_now(data)
    return render(request, 'core/about_us.html', data)


def home(request):
    return redirect('posts')
