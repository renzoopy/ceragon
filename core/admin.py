from django.contrib import admin
from unfold.admin import ModelAdmin
from core.models import Author, Book


@admin.register(Author)
class AuthorAdmin(ModelAdmin):
    list_display = ("first_name", "last_name", "birth_date")
    search_fields = ("first_name", "last_name")
    ordering = ("last_name",)


@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ("title", "published_at", "display_authors")
    search_fields = ("title", "isbn")
    ordering = ("title",)
    filter_horizontal = ("authors",)

    def display_authors(self, obj):
        return ", ".join(str(author) for author in obj.authors.all())

    display_authors.short_description = "Authors"
