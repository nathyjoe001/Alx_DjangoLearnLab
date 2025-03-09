from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets


# Create your views here.
# api/views.py
from django.http import JsonResponse

  
def example_view(request):
    return JsonResponse({'message': 'This is an example endpoint'})

def other_view(request):
    return JsonResponse({'message': 'This is another endpoint'})



class BookList(generics.ListAPIView):
    queryset = Book.objects.all()  # Query to fetch all books from the database
    serializer_class = BookSerializer  # Use the BookSerializer to convert model data to JSON


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()  # Query all books
    serializer_class = BookSerializer  # Use the BookSerializer to convert model instances to JSON




