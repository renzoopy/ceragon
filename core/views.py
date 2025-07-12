from rest_framework import viewsets, filters
from core.models import Author, Book
from core.serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage authors.
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["first_name", "last_name"]
    ordering_fields = ["first_name", "last_name", "birth_date"]


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage books.
    """

    queryset = Book.objects.prefetch_related("authors").all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "isbn", "authors__first_name", "authors__last_name"]
    ordering_fields = ["title", "published_at"]
