
# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from django.views.generic import DetailView
from .models import Library

class LibraryDetailView(DetailView):
    model = Library
    template_name = "library_detail.html"
    context_object_name = "library"

def list_books(request):
    books = Book.objects.all()
    book_list = "<h1>Books Available:</h1><ul>"
    for book in books:
        book_list += f"<li>{book.title} by {book.author.name}</li>"
    book_list += "</ul>"
    return HttpResponse(book_list)



