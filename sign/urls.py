from django.urls import path
from .views import upgrade_to_authors


urlpatterns = [
    path('upgrade/', upgrade_to_authors, name='upgrade'),
]