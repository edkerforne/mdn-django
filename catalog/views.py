from django.shortcuts import render
from .models import Author, Book, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate book and book instance counts
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_authors = Author.objects.count()

    # Count available books
    num_available = BookInstance.objects.filter(status__exact='a').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_available': num_available,
        'num_authors': num_authors
    }

    # Render HTML template index.html with data in the context variable
    return render(request, 'index.html', context=context)