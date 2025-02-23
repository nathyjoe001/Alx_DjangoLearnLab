
# Create your views here.
from django.shortcuts import render
from django.views.generic.detail import DetailView  # Correct import
from .models import Book, Library
from django.http import HttpResponse

# Function-based view to list all books


def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


