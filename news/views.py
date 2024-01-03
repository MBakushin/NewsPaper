from django.http import JsonResponse
from django.shortcuts import render, reverse, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView,\
                                 DeleteView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .filters import PostFilter
from .forms import NewsForm
from .models import *


# class AuthorListView(ListView):
#     model = Author
#     ordering = 'user__username'
#     template_name = 'authors.html'
#     context_object_name = 'authors'
#
#
# class AuthorDetailView(DetailView):
#     model = Author
#     template_name = 'author.html'
#     context_object_name = 'author'


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
    template_name = 'news/allnews.html'
    context_object_name = 'allnews'
    paginate_by = 3


class NewsDetailView(BecameAuthor, DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'news_detail'


class NewsSearchView(BecameAuthor, ListView):
    model = Post
    template_name = 'news/search.html'
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


class NewsAddView(BecameAuthor, PermissionRequiredMixin, CreateView):
    template_name = 'news/news_add.html'
    context_object_name = 'news'
    form_class = NewsForm
    permission_required = ('news.add_post', )


class NewsEditView(BecameAuthor, PermissionRequiredMixin, UpdateView):
    template_name = 'news/news_add.html'
    form_class = NewsForm
    permission_required = ('news.change_post', )

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return Post.objects.get(pk=pk)


class NewsDeleteView(BecameAuthor, PermissionRequiredMixin, DeleteView):
    template_name = 'news/news_delete.html'
    context_object_name = 'news'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.view_post', )


class NewsCategoriesView(BecameAuthor, ListView):
    model = Category
    template_name = 'news/categories.html'
    context_object_name = 'categories'


class NewsCategoryView(BecameAuthor, DetailView):
    model = Category
    template_name = 'news/category.html'
    context_object_name = 'category'


@login_required
def change_sub(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    if user in category.get_subs():
        category.subscribers.remove(user)
        message = "You've unsubscribed from "
    else:
        category.subscribers.add(user)
        message = "You've subscribed to "
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})
