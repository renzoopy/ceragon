from rest_framework import serializers
from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model.
    """

    book_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Author
        fields = ("id", "first_name", "last_name", "birth_date", "bio", "book_count")


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer used for creating and updating Book instances.
    Accepts a list of author IDs for the 'authors' field.
    """

    authors = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = Book
        fields = (
            "title",
            "isbn",
            "published_at",
            "description",
            "authors",
        )


class BookReadSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for Book model.
    Returns nested author data for the 'authors' field.
    """

    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "isbn",
            "published_at",
            "description",
            "authors",
        )
