import uuid  # Required for unique book instances

from django.db import models
from django.urls import (
    reverse,
)
from django.db.models import UniqueConstraint  # Constrains fields to unique values
from django.db.models.functions import Lower  # Returns lower cased value of field
from django.utils.translation import gettext_lazy as _

from .constants import (
    CHAR_MAX_LENGTH,
    TEXT_MAX_LENGTH,
    ISBN_MAX_LENGTH,
    STATUS_MAX_LENGTH,
)


class Genre(models.Model):
    """Model representing a book genre."""

    name = models.CharField(
        max_length=CHAR_MAX_LENGTH,
        unique=True,
        help_text=_("Enter a book genre (e.g. Science Fiction, French Poetry etc.)"),
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse("genre-detail", args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower("name"),
                name="genre_name_case_insensitive_unique",
                violation_error_message="Genre already exists (case insensitive match)",
            ),
        ]


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""

    title = models.CharField(max_length=CHAR_MAX_LENGTH)
    author = models.ForeignKey("Author", on_delete=models.RESTRICT, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books.
    # Author as a string rather than object because it hasn't been declared yet in file.

    summary = models.TextField(
        max_length=TEXT_MAX_LENGTH, help_text=_("Enter a brief description of the book")
    )
    isbn = models.CharField(
        "ISBN",
        max_length=ISBN_MAX_LENGTH,
        unique=True,
        help_text=_(
            '13 Character <a href="https://www.isbn-international.org/content/what-isbn'
            '">ISBN number</a>'
        ),
    )

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text=_("Select a genre for this book"))

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse("book-detail", args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ", ".join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = "Genre"


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text=_("Unique ID for this particular book across whole library"),
    )
    book = models.ForeignKey("Book", on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=CHAR_MAX_LENGTH)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    )

    status = models.CharField(
        max_length=STATUS_MAX_LENGTH,
        choices=LOAN_STATUS,
        blank=True,
        default="m",
        help_text=_("Book availability"),
    )

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.id} ({self.book.title})"


class Author(models.Model):
    """Model representing an author."""

    first_name = models.CharField(max_length=CHAR_MAX_LENGTH)
    last_name = models.CharField(max_length=CHAR_MAX_LENGTH)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("Died", null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.last_name}, {self.first_name}"
