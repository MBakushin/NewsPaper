from django.urls import path
from .views import *


urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('add/', NewsCreate.as_view(), name='news_add'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete', NewsDelete.as_view(), name='news_delete'),
]