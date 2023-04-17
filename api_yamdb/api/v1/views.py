from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.permissions import (
    SAFE_METHODS,
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from api.v1.filters import TitleFilter
from api.v1.permissions import (
    IsAdminOrReadOnly,
    IsAdminUser,
    IsAuthorOrModerAdminPermission,
)
from api.v1.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignupSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    UserSerializer,
    UsersMeSerializer,
    YamdbTokenObtainPairSerializer,
)
from api.v1.utils import send_confirmation_code
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAuthenticated, IsAdminUser)


class UsersMeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        me = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(me)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        me = get_object_or_404(User, username=request.user.username)
        serializer = UsersMeSerializer(me, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class YamdbTokenObtainPairView(TokenObtainPairView):
    serializer_class = YamdbTokenObtainPairSerializer


class SignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if User.objects.filter(username=request.data.get('username'),
                               email=request.data.get('email')).exists():
            send_confirmation_code(request)
            return Response(request.data, status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_confirmation_code(request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CreateListDestroyViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score'),
    ).order_by('name')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    )

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModerAdminPermission,
                          IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModerAdminPermission,
                          IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title)
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title)
        serializer.save(author=self.request.user, review=review)
