import django_filters
from django.db.models import Count
from core.models import Author, Book


class AuthorFilter(django_filters.FilterSet):
    """
    Custom filters for Author model.
    Allows filtering by min/max birth date and book count.
    """

    min_birth_date = django_filters.DateFilter(
        field_name="birth_date", lookup_expr="gte"
    )
    max_birth_date = django_filters.DateFilter(
        field_name="birth_date", lookup_expr="lte"
    )
    min_books = django_filters.NumberFilter(method="filter_min_books")
    max_books = django_filters.NumberFilter(method="filter_max_books")

    class Meta:
        model = Author
        fields = ["min_birth_date", "max_birth_date", "min_books", "max_books"]

    def filter_min_books(self, queryset, name, value):
        return queryset.annotate(book_count=Count("books")).filter(
            book_count__gte=value
        )

    def filter_max_books(self, queryset, name, value):
        return queryset.annotate(book_count=Count("books")).filter(
            book_count__lte=value
        )


class BookFilter(django_filters.FilterSet):
    """
    Custom filters for Book model.
    Allows filtering by published date range.
    """

    min_published = django_filters.DateFilter(
        field_name="published_at", lookup_expr="gte"
    )
    max_published = django_filters.DateFilter(
        field_name="published_at", lookup_expr="lte"
    )
    author = django_filters.NumberFilter(field_name="authors__id", lookup_expr="exact")
    authors = django_filters.BaseInFilter(field_name="authors__id", lookup_expr="in")

    class Meta:
        model = Book
        fields = ["min_published", "max_published", "author", "authors"]
