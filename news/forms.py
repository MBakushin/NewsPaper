from django.forms import ModelForm
from .models import Post, Category


class NewsForm(ModelForm):
    class Meta:
        model = Post
        fields = ['note', 'categories', 'header', 'text', 'author']
