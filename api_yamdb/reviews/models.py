from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата отзыва',
        auto_now_add=True,
        db_index=True
    )
    text = models.TextField()
    score = models.IntegerField(
        'Оценка',
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name="unique_review")
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата комментария',
        auto_now_add=True,
        db_index=True
    )
    text = models.TextField()

    def __str__(self):
        return self.author
        
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
