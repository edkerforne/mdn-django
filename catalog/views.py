from django.shortcuts import render
from .models import Author, Book, BookInstance, Genre
from django.views import generic

def index(request):
    """View function for home page of site."""

    # Generate book and book instance counts
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_authors = Author.objects.count()

    # Count available books
    num_available = BookInstance.objects.filter(status__exact='a').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_available': num_available,
        'num_authors': num_authors,
        'num_visits': num_visits
    }

    # Render HTML template index.html with data in the context variable
    return render(request, 'index.html', context=context)

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book