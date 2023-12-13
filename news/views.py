from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView,\
                                 DeleteView, View

from .filters import PostFilter
from .forms import NewsForm
from .models import *


class AuthorListView(ListView):
    model = Author
    ordering = 'user__username'
    template_name = 'authors.html'
    context_object_name = 'authors'


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author.html'
    context_object_name = 'author'


class BecameAuthor:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(
            name='authors').exists()
        context['is_authors'] = self.request.user.groups.filter(
            name='authors').exists()
        return context


class NewsListView(BecameAuthor, ListView):
    model = Post
    ordering = '-time_to_update'
    template_name = 'allnews.html'
    context_object_name = 'allnews'
    paginate_by = 3


class NewsDetailView(BecameAuthor, DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'


class NewsSearchView(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    ordering = ['-time_to_update']

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter()
        }


class NewsAddView(BecameAuthor, LoginRequiredMixin, CreateView):
    template_name = 'news_add.html'
    context_object_name = 'news'
    form_class = NewsForm


class NewsEditView(BecameAuthor, LoginRequiredMixin, UpdateView):
    template_name = 'news_add.html'
    form_class = NewsForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDeleteView(BecameAuthor, LoginRequiredMixin, DeleteView):
    template_name = 'news_delete.html'
    context_object_name = 'news'
    queryset = Post.objects.all()
    success_url = '/news/'
