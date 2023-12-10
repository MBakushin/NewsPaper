from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *


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


class NewsDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
