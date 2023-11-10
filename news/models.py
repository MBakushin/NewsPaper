from django.db import models
from django.contrib.auth.models import User  # mb need alias like authUser
from news.addition import *


class Author(models.Model):
    rating = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        self.rating = 0
        # all author's posts rating multiply by 3
        r1 = Post.objects.filter(author=self.pk).values('rating')
        for r in r1:
            self.rating += r['rating']
        self.rating *= 3

        # all author's comments rating
        r2 = Comment.objects.filter(user=self.user).values('rating')
        for r in r2:
            self.rating += r['rating']

        # all comment to author's posts rating
        post = Post.objects.filter(author=self.pk)
        for p in post:
            r3 = Comment.objects.filter(post=p).values('rating')
            for r in r3:
                self.rating += r['rating']

        self.save()
        return self.rating


class Category(models.Model):
    title = models.CharField(max_length=56, unique=True)

    posts = models.ManyToManyField('Post', through='PostCategory')


class Post(models.Model, Grade):
    note = models.CharField(max_length=2, choices=NOTES, default=news)
    time_to_create = models.DateTimeField(auto_now_add=True)
    time_to_update = models.DateTimeField(auto_now=True)
    header = models.CharField(max_length=56)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', through='PostCategory')

    def preview(self):
        return f"{self.text[:125]}..."


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model, Grade):
    time_to_create = models.DateTimeField(auto_now_add=True)
    time_to_update = models.DateTimeField(auto_now=True)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
