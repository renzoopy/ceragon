from django.db import models
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    """
    Represents an author who may have written one or more books.
    """

    first_name = models.CharField(
        verbose_name=_("First name"),
        max_length=100
    )
    last_name = models.CharField(
        verbose_name=_("Last name"),
        max_length=100
    )
    birth_date = models.DateField(
        verbose_name=_("Birth date"),
        null=True,
        blank=True
    )
    bio = models.TextField(
        verbose_name=_("Biography"),
        blank=True,
        default=""
    )
    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated at"), auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")


class Book(models.Model):
    """
    Represents a book which can have multiple authors.
    """

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=200
    )
    isbn = models.CharField(
        verbose_name=_("ISBN"),
        max_length=13,
        blank=True
    )
    published_at = models.DateField(
        verbose_name=_("Published Date"),
        null=True,
        blank=True
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True
    )
    authors = models.ManyToManyField(
        Author,
        verbose_name=_("Authors"),
        related_name="books"
    )
    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated at"), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
