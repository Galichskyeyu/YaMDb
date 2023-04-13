from django.contrib import admin
from .models import Comment, Review, Title, Category, Genre, GenreTitle, Titles


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'score', 'author', 'title')
    search_fields = ('title', 'author')
    list_filter = ('score', 'text',)
    empty_value_display = '-пусто-'


admin.site.register(Review, ReviewsAdmin)
admin.site.register(Comment)
admin.site.register(Titles)
admin.site.register(Genre)
admin.site.register(GenreTitle)
admin.site.register(Category)
