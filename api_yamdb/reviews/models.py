from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Модель типов произведений."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров произведний."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    """Модель произвдений."""

    name = models.TextField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Промежуточная модель для связи жанров и произведений."""

    title_id = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        null=True,
    )
    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        null=True,
    )
