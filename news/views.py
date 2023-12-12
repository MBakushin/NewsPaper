from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator

from .models import *
from .filters import PostFilter


class AuthorList(ListView):
    model = Author
    ordering = 'user__username'
    template_name = 'authors.html'
    context_object_name = 'authors'


class AuthorDetail(DetailView):
    model = Author
    template_name = 'author.html'
    context_object_name = 'author'


class NewsList(ListView):
    model = Post
    ordering = '-time_to_update'
    template_name = 'allnews.html'
    context_object_name = 'allnews'
    paginate_by = 2


class NewsDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'


class NewsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    ordering = ['-time_to_update']
    paginate_by = 3

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self,*args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter()
        }
