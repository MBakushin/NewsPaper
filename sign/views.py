from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import CreateView
from .models import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = 'news/'
