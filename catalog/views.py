import datetime
from django.shortcuts import render
from catalog.models import Author, Book, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from catalog.forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView


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


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """List view for books on loan by current user."""
    model = BookInstance
    template_name = 'catalog/books_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due')


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """List view for all books currently on loan (only for librarians)."""
    permission_required = 'catalog.can_mark_returned'

    model = BookInstance
    template_name = 'catalog/books_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View for renewing a specific book instance by a librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # Process form data on POST.
    if request.method == 'POST':

        # Create and populate a form instance with request data.
        form = RenewBookForm(request.POST)

        # Check if form is valid, write to the model and redirect to borrowed list.
        if form.is_valid():
            book_instance.due = form.cleaned_data['due']
            book_instance.save()
            return HttpResponseRedirect(reverse('borrowed'))

    # Render form on GET.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'due': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.add_author'
    model = Author
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prefix'] = 'Create'
        return context


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.change_author'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prefix'] = 'Update'
        return context


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.delete_author'
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.add_book'
    model = Book
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prefix'] = 'Create'
        return context


class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.change_book'
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prefix'] = 'Update'
        return context


class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.delete_book'
    model = Book
    success_url = reverse_lazy('books')
