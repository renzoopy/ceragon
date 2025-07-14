import pytest
from datetime import date
from rest_framework.test import APIClient
from core.models import Author, Book

pytestmark = pytest.mark.django_db


class TestBookAPI:
    """Test suite for the Book API."""

    def setup_method(self):
        self.client = APIClient()
        self.author1 = Author.objects.create(first_name="George", last_name="Orwell")
        self.author2 = Author.objects.create(first_name="J.R.R.", last_name="Tolkien")
        self.book_payload = {
            "title": "1984",
            "isbn": "9780451524935",
            "published_at": "1949-06-08",
            "authors": [self.author1.id],
        }
        self.book = Book.objects.create(title="Animal Farm")
        self.book.authors.add(self.author1)

    def test_create_book_success(self):
        """✅ Test creating a book successfully."""
        response = self.client.post("/books/", self.book_payload, format="json")

        if response.status_code != 201:
            print("Error details:", response.data)

        assert response.status_code == 201
        new_book = Book.objects.get(title="1984")
        assert new_book.isbn == "9780451524935"
        assert new_book.authors.filter(id=self.author1.id).exists()

    def test_create_book_missing_required_field_fails(self):
        """❌ Test creating a book fails if 'title' is missing."""
        payload = self.book_payload.copy()
        del payload["title"]
        response = self.client.post("/books/", payload, format="json")
        assert response.status_code == 400

    def test_create_book_with_nonexistent_author_fails(self):
        """❌ Test creating a book fails with a non-existent author ID."""
        payload = self.book_payload.copy()
        payload["authors"] = [999]
        response = self.client.post("/books/", payload, format="json")
        assert response.status_code == 400

    def test_list_books(self):
        """✅ Test listing all books."""
        Book.objects.create(title="The Hobbit")
        response = self.client.get("/books/")
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_retrieve_book_success(self):
        """✅ Test retrieving a specific book."""
        response = self.client.get(f"/books/{self.book.id}/")
        assert response.status_code == 200
        assert response.data["title"] == "Animal Farm"
        assert response.data["authors"][0]["first_name"] == "George"

    def test_retrieve_book_not_found(self):
        """❌ Test retrieving a non-existent book."""
        response = self.client.get("/books/999/")
        assert response.status_code == 404

    def test_update_book_partial_patch(self):
        """✅ Test partially updating a book with PATCH."""
        payload = {"description": "A political allegory."}
        response = self.client.patch(f"/books/{self.book.id}/", payload, format="json")
        self.book.refresh_from_db()
        assert response.status_code == 200
        assert self.book.description == "A political allegory."
        assert self.book.title == "Animal Farm"

    def test_update_book_authors_patch(self):
        """✅ Test updating a book's authors."""
        payload = {"authors": [self.author1.id, self.author2.id]}
        response = self.client.patch(f"/books/{self.book.id}/", payload, format="json")
        self.book.refresh_from_db()
        assert response.status_code == 200
        assert self.book.authors.count() == 2
        assert self.book.authors.filter(last_name="Tolkien").exists()

    def test_update_book_not_found(self):
        """❌ Test updating a non-existent book."""
        response = self.client.put("/books/999/", self.book_payload, format="json")
        assert response.status_code == 404

    def test_delete_book_success(self):
        """✅ Test deleting an existing book."""
        response = self.client.delete(f"/books/{self.book.id}/")
        assert response.status_code == 204
        assert not Book.objects.filter(id=self.book.id).exists()

    def test_delete_book_not_found(self):
        """❌ Test deleting a non-existent book."""
        response = self.client.delete("/books/999/")
        assert response.status_code == 404
