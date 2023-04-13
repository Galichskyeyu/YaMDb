from django.contrib import admin

from .models import Category, Genre, GenreTitle, Titles

admin.site.register(Titles)
admin.site.register(Genre)
admin.site.register(GenreTitle)
admin.site.register(Category)
