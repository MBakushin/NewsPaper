from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )


admin.site.register(Author)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post)
admin.site.register(Comment)
