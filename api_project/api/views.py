from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

# Create your views here.

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()  # Query to fetch all books from the database
    serializer_class = BookSerializer  # Use the BookSerializer to convert model data to JSON
