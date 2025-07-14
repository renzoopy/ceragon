import pytest
from rest_framework.test import APIClient
from core.models import Author

pytestmark = pytest.mark.django_db


class TestAuthorAPI:
    """Test suite for the Author API."""

    def setup_method(self):
        """Setup for every test method."""
        self.client = APIClient()
        self.author_payload = {
            "first_name": "George",
            "last_name": "Orwell",
            "birth_date": "1903-06-25",
            "bio": "English novelist, essayist, journalist and critic.",
        }
        self.author = Author.objects.create(first_name="Jane", last_name="Austen")

    def test_create_author_success(self):
        """✅ Test creating an author successfully."""
        response = self.client.post("/authors/", self.author_payload, format="json")
        assert response.status_code == 201
        assert Author.objects.filter(first_name="George", last_name="Orwell").exists()

    def test_create_author_missing_required_field_fails(self):
        """❌ Test creating an author fails if a required field is missing."""
        payload = self.author_payload.copy()
        del payload["first_name"]
        response = self.client.post("/authors/", payload, format="json")
        assert response.status_code == 400

    def test_create_author_invalid_data_fails(self):
        """❌ Test creating an author fails with invalid data."""
        payload = self.author_payload.copy()
        payload["birth_date"] = "not-a-date"
        response = self.client.post("/authors/", payload, format="json")
        assert response.status_code == 400

    def test_create_author_exceeds_max_length_fails(self):
        """❌ Test creating an author fails if a field exceeds max length."""
        payload = self.author_payload.copy()
        payload["first_name"] = "a" * 101  # max_length is 100
        response = self.client.post("/authors/", payload, format="json")
        assert response.status_code == 400

    def test_list_authors(self):
        """✅ Test listing all authors."""
        Author.objects.create(first_name="Leo", last_name="Tolstoy")
        response = self.client.get("/authors/")
        assert response.status_code == 200
        assert len(response.data) == 2  # Jane Austen and Leo Tolstoy

    def test_retrieve_author_success(self):
        """✅ Test retrieving a specific author."""
        response = self.client.get(f"/authors/{self.author.id}/")
        assert response.status_code == 200
        assert response.data["first_name"] == "Jane"

    def test_retrieve_author_not_found(self):
        """❌ Test retrieving a non-existent author."""
        response = self.client.get("/authors/999/")
        assert response.status_code == 404

    def test_update_author_partial_patch(self):
        """✅ Test partially updating an author with PATCH."""
        payload = {"bio": "An updated bio."}
        response = self.client.patch(
            f"/authors/{self.author.id}/", payload, format="json"
        )
        self.author.refresh_from_db()
        assert response.status_code == 200
        assert self.author.bio == "An updated bio."
        assert self.author.first_name == "Jane"  # Unchanged

    def test_update_author_full_put(self):
        """✅ Test fully updating an author with PUT."""
        response = self.client.put(
            f"/authors/{self.author.id}/", self.author_payload, format="json"
        )
        self.author.refresh_from_db()
        assert response.status_code == 200
        assert self.author.first_name == "George"
        assert self.author.last_name == "Orwell"

    def test_update_author_not_found(self):
        """❌ Test updating a non-existent author."""
        response = self.client.put("/authors/999/", self.author_payload, format="json")
        assert response.status_code == 404

    def test_delete_author_success(self):
        """✅ Test deleting an existing author."""
        response = self.client.delete(f"/authors/{self.author.id}/")
        assert response.status_code == 204
        assert not Author.objects.filter(id=self.author.id).exists()

    def test_delete_author_not_found(self):
        """❌ Test deleting a non-existent author."""
        response = self.client.delete("/authors/999/")
        assert response.status_code == 404
