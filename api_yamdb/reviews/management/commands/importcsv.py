import sys
from csv import DictReader
from os.path import exists
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


class Command(BaseCommand):

    def objects_creator(model, row, response):
        if model == User:
            User.objects.create(
                id=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6]
            )
        if model == Category:
            Category.objects.create(
                id=row[0],
                name=row[1],
                slug=row[2],
            )
        if model == Comment:
            Comment.objects.create(
                id=row[0],
                review=Review.objects.get(id=row[1]),
                text=row[2],
                author=User.objects.get(id=row[3]),
                pub_date=row[4],
            )
        if model == Genre:
            Genre.objects.create(
                id=row[0],
                name=row[1],
                slug=row[2],
            )
        if model == GenreTitle:
            GenreTitle.objects.create(
                id=row[0],
                title=Title.objects.get(id=row[1]),
                genre=Genre.objects.get(id=row[2]),
            )
        if model == Review:
            Review.objects.create(
                id=row[0],
                title=Title.objects.get(id=row[1]),
                text=row[2],
                author=User.objects.get(id=row[3]),
                score=row[4],
                pub_date=row[5],
            )
        if model == Title:
            Title.objects.create(
                id=row[0],
                name=row[1],
                year=row[2],
                category=Category.objects.get(
                    id=row[3]
                ),
            )
        
    def handle(self, *args, **options):
        for filename, model in MODELS.items():
            csv_file = find(f'data/{filename}.csv')
            for row in DictReader(open(csv_file, encoding='utf-8')):
                self.objects_creator(model, row)
            print('Новые объекты добавлены.')