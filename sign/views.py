from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from news.models import Author, Category


@login_required
def upgrade_to_authors(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')

    authors_group.user_set.add(user)
    Author.objects.create(user=user)
    return redirect('/')
