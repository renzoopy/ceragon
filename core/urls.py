from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import AuthorViewSet, BookViewSet, TopAuthorsAPIView, StatsAPIView

router = DefaultRouter()

router.register("authors", AuthorViewSet, basename="authors")
router.register("books", BookViewSet, basename="books")

urlpatterns = [
    path("", include(router.urls)),
    path("top-authors/", TopAuthorsAPIView.as_view(), name="top-authors"),
    path("stats/", StatsAPIView.as_view(), name="stats"),
]
