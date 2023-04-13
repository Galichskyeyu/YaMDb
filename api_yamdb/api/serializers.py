from rest_framework import serializers

from reviews.models import Category, Genre, Titles


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitlesSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',

            'description',
            'genre',
            'category'
        )
        model = Titles
