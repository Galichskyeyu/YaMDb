from rest_framework import serializers
from reviews.models import Comment, Review


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True
                                          )
    title = serializers.SlugRelatedField(slug_field='id',
                                         read_only=True
                                         )

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True
                                          )
    review = serializers.SlugRelatedField(slug_field='id',
                                          read_only=True
                                          )

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date',)
        read_only_fields = ('id', 'author', 'pub_date',)
        
