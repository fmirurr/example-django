from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Author, Book, BookInstance, Genre

# Create your views here.


def index(request):
    # Numero de instancias
    num_books = Book.objects.all().count()
    num_instaces = BookInstance.objects.all().count()
    # Libros disponibles (a)
    num_instaces_avalible = BookInstance.objects.filter(
        status__exact='a').count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {'num_books': num_books,
               'num_instaces': num_instaces,
               'num_instaces_avalible': num_instaces_avalible,
               'num_authors': num_authors,
               'num_visits': num_visits
               }

    return render(
        request,
        'index.html',
        context=context
    )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
