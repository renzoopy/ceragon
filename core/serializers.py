from rest_framework import serializers
from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model.
    """

    class Meta:
        model = Author
        fields = ("id", "first_name", "last_name", "birth_date", "bio")


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model.
    Shows nested authors on read,
    and accepts list of author IDs on write.
    """

    authors = AuthorSerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), many=True, write_only=True, source="authors"
    )

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "isbn",
            "published_at",
            "description",
            "authors",
            "author_ids",
        )
