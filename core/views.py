from django.db.models import Count, Avg
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Author, Book
from core.serializers import AuthorSerializer, BookSerializer, BookReadSerializer
from core.filters import AuthorFilter, BookFilter


class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage authors.
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filterset_class = AuthorFilter
    search_fields = ["first_name", "last_name"]
    ordering_fields = ["first_name", "last_name", "birth_date"]


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage books.
    """

    queryset = Book.objects.prefetch_related("authors").all()
    serializer_class = BookSerializer
    filterset_class = BookFilter
    search_fields = ["title", "isbn", "authors__first_name", "authors__last_name"]
    ordering_fields = ["title", "published_at"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return BookReadSerializer
        return BookSerializer


class TopAuthorsAPIView(APIView):
    """
    Returns top authors by number of books written.
    """

    def get(self, request):
        top_authors = Author.objects.annotate(book_count=Count("books")).order_by(
            "-book_count"
        )[:10]
        print(top_authors.first().__dict__)
        serializer = AuthorSerializer(top_authors, many=True)
        return Response(serializer.data)


class StatsAPIView(APIView):
    """
    Returns global statistics about books and authors.
    """

    def get(self, request):
        total_books = Book.objects.count()
        total_authors = Author.objects.count()
        avg_books = Author.objects.annotate(num=Count("books")).aggregate(
            avg=Avg("num")
        )["avg"]

        return Response(
            {
                "total_books": total_books,
                "total_authors": total_authors,
                "avg_books_per_author": round(avg_books or 0, 2),
            }
        )
