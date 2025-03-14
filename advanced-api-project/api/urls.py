# api/urls.py
from django.urls import path
from api.views import BookListView, BookCreateView, BookDetailView,BookUpdateView,BookDeleteView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),  # List and create books
    path('books/create/', BookCreateView.as_view(), name='book-create'),  # Create a new book
    path('books/<int:pk>/',BookDetailView.as_view(), name='book-detail'),  # Retrieve a single book by ID
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),  # Update a book
    path('books/delete/<int:pk>/',BookDeleteView.as_view(), name='book-delete'),  # Delete a book
]



