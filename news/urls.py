from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *


urlpatterns = [
    path('', cache_page(60*5)(NewsListView.as_view()), name='news_list'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('search/', NewsSearchView.as_view(), name='news_search'),
    path('add/', NewsAddView.as_view(), name='news_add'),
    path('<int:pk>/edit/', NewsEditView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('categories/', NewsCategoriesView.as_view(), name='news_categories'),
    path('categories/<int:pk>/', NewsCategoryView.as_view(),
         name='news_category'),
path('categories/<int:pk>/sub/', change_sub, name='sub'),
]
