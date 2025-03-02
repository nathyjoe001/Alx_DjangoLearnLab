
from django.shortcuts import render, redirect
from .forms import ExampleForm
from django.contrib.auth.decorators import permission_required
from .models import Book

@permission_required('bookshelf.view_book', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})
# Create your views here.



def add_book(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")  # Ensure you have a URL named 'book_list'
    else:
        form = ExampleForm()

    return render(request, "bookshelf/book_form.html", {"form": form})
