from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import CategoryViewSet, GenreViewSet, TitlesViewSet

router = SimpleRouter()
router.register('titles', TitlesViewSet, basename='titles')
router.register('genre', GenreViewSet, basename='genre')
router.register('categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('', include(router.urls)),
]
