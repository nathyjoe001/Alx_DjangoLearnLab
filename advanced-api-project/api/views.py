# api/views.py
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated

# List and Create views for Book model
class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []  # Allow unauthenticated access for list view

#class BookCreateView(generics.CreateAPIView):
    #queryset = Book.objects.all()
    #serializer_class = BookSerializer

   # def perform_create(self, serializer):
        # Custom behavior for book creation can go here
       # serializer.save()

# Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []  # Allow unauthenticated access for detail view

# Update an existing book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can update

# Delete a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]  # Only authenticated users can delete
