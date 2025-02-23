from django.shortcuts import render
from django.views.generic.detail import DetailView  # Import DetailView
from .models import Book, Library  # Ensure Library is imported

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display details of a library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

