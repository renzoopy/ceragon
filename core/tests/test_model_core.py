import pytest
from django.core.exceptions import ValidationError
from core.models import Author, Book


class TestUnitModels:
    """
    Unit tests for model methods and representations.
    These tests are isolated and do not require the database.
    """

    def test_author_model_str(self):
        """Test the string representation of the Author model."""
        author = Author(first_name="Gabriel", last_name="García Márquez")
        assert str(author) == "Author: Gabriel García Márquez"

    def test_book_model_str(self):
        """Test the string representation of the Book model."""
        book = Book(title="One Hundred Years of Solitude")
        assert str(book) == "One Hundred Years of Solitude"

    def test_author_full_name(self):
        author = Author(first_name="George", last_name="Orwell")
        assert author.full_name == "George Orwell"

    def test_book_requires_title(self):
        book = Book(title="")
        with pytest.raises(ValidationError):
            book.full_clean()
