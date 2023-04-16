from csv import DictReader
from django.contrib.staticfiles.finders import find
from django.core.management import BaseCommand

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)


MODELS = {
    'users': User,
    'category': Category,
    'titles': Title,
    'review': Review,
    'comments': Comment,
    'genre': Genre,
    'genre_title': GenreTitle,
}


def objects_creator(model, row):
    if model == User:
        User.objects.get_or_create(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            role=row['role'],
            bio=row['bio'],
            first_name=row['first_name'],
            last_name=row['last_name']
        )
    if model == Category:
        Category.objects.get_or_create(
            id=row['id'],
            name=row['name'],
            slug=row['slug'],
        )
    if model == Comment:
        Comment.objects.get_or_create(
            id=row['id'],
            review=Review.objects.get(id=row['review_id']),
            text=row['text'],
            author=User.objects.get(id=row['author']),
            pub_date=row['pub_date'],
        )
    if model == Genre:
        Genre.objects.get_or_create(
            id=row['id'],
            name=row['name'],
            slug=row['slug'],
        )
    if model == GenreTitle:
        GenreTitle.objects.get_or_create(
            id=row['id'],
            title=Title.objects.get(id=row['title_id']),
            genre=Genre.objects.get(id=row['genre_id']),
        )
    if model == Review:
        Review.objects.get_or_create(
            id=row['id'],
            title=Title.objects.get(id=row['title_id']),
            text=row['text'],
            author=User.objects.get(id=row['author']),
            score=row['score'],
            pub_date=row['pub_date'],
        )
    if model == Title:
        Title.objects.get_or_create(
            id=row['id'],
            name=row['name'],
            year=row['year'],
            category=Category.objects.get(
                id=row['category']
            ),
        )


class Command(BaseCommand):

    def handle(self, *args, **options):
        for filename, model in MODELS.items():
            csv_file = find(f'data/{filename}.csv')
            for row in DictReader(open(csv_file, encoding='utf-8')):
                objects_creator(model, row)
            print('Новые объекты добавлены.')
