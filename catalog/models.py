from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns.
import uuid # Required for unique book instances

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=32, help_text='Enter a book genre (e.g. Adventure, Science Fiction...)')

    def __str__(self):
        """String representing the model object."""
        return self.name

class Language(models.Model):
    """Model representing a language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=32, help_text="Enter the book's natural language (e.g. English, French...)")

    def __str__(self):
        """String representing the model object."""
        return self.name

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=128)

    # Foreign key used because book can only have one author, but authors can have multiple books.
    # Author as a string rather than object because it hasn't been declared yet in the file.
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1024, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13-character ISBN number')

    # Many to many used because genres can contain many books, and books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String representing the model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Returns a comma-separated string representation of the book's genres."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. one that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across the whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=128, help_text='Publisher information')
    due = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability'
    )

    class Meta:
        ordering = ['due']
    
    def __str__(self):
        """String representing the model object."""
        return f'{self.id} ({self.book.title})'
    
class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def get_absolute_url(self):
        """Returns the URL to access a particular author."""
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        """String representing the model object."""
        return f'{self.first_name} {self.last_name}'
