from django.contrib import admin
from .models import *


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = ('title', )
    search_fields = ('title', )


class PostAdmin(admin.ModelAdmin):
    list_display = ('note', 'header', 'time_to_create', 'time_to_update', )
    list_filter = ('note', 'header', 'time_to_create', 'time_to_update', )
    search_fields = ('note', 'header', 'time_to_create', 'time_to_update', )


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
