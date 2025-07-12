import random
import traceback
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model
from faker import Faker
from core.models import Author, Book

NUM_AUTHORS = 50
NUM_BOOKS = 250
SUPERUSER_USERNAME = "admin"
SUPERUSER_EMAIL = "admin@ceragon.com"
SUPERUSER_PASS = "Challenge.1"


class Command(BaseCommand):
    """
    Django command to initialize the database with test data.

    Usage: python manage.py initialize
    """

    help = "Populates the database with a set of realistic authors and books."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting database initialization..."))

        User = get_user_model()

        # --- Superuser Creation ---
        # We do this outside the transaction to avoid issues if the user already exists.
        self.stdout.write(f"Checking for superuser '{SUPERUSER_USERNAME}'...")
        if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
            self.stdout.write(f"Creating superuser '{SUPERUSER_USERNAME}'...")
            User.objects.create_superuser(
                username=SUPERUSER_USERNAME,
                email=SUPERUSER_EMAIL,
                password=SUPERUSER_PASS,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Superuser '{SUPERUSER_USERNAME}' created.")
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"Superuser '{SUPERUSER_USERNAME}' already exists. Skipping."
                )
            )

        # --- Data Population ---

        try:
            with transaction.atomic():
                self.stdout.write("Cleaning the database...")
                Author.objects.all().delete()
                Book.objects.all().delete()
                self.stdout.write(self.style.SUCCESS("Database cleaned."))

                fake = Faker()

                self.stdout.write(f"Creating {NUM_AUTHORS} authors...")
                authors = []
                for _ in range(NUM_AUTHORS):
                    author = Author(
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        birth_date=fake.date_of_birth(minimum_age=25, maximum_age=90),
                        bio=fake.paragraph(nb_sentences=5),
                    )
                    authors.append(author)

                Author.objects.bulk_create(authors)
                self.stdout.write(self.style.SUCCESS(f"{NUM_AUTHORS} authors created."))

                all_authors = list(Author.objects.all())

                self.stdout.write(f"Creating {NUM_BOOKS} books...")
                books = []
                for _ in range(NUM_BOOKS):
                    title = " ".join(
                        word.capitalize()
                        for word in fake.words(nb=random.randint(2, 6))
                    )

                    book = Book(
                        title=title,
                        isbn=fake.isbn13().replace("-", ""),
                        published_at=fake.date_between(
                            start_date="-50y", end_date="today"
                        ),
                        description=fake.paragraph(nb_sentences=10),
                    )
                    books.append(book)

                created_books = Book.objects.bulk_create(books)

                self.stdout.write("Assigning authors to books...")

                through_model = Book.authors.through
                assignments = []

                for book in created_books:
                    num_book_authors = random.randint(1, 3)
                    sampled_authors = random.sample(all_authors, num_book_authors)

                    for author in sampled_authors:
                        assignments.append(
                            through_model(book_id=book.id, author_id=author.id)
                        )

                through_model.objects.bulk_create(assignments)
                self.stdout.write(
                    self.style.SUCCESS(f"{NUM_BOOKS} books created and assigned.")
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"An error occurred: {e}. {traceback.format_exc()}")
            )
            raise

        self.stdout.write(self.style.SUCCESS("Success!"))
