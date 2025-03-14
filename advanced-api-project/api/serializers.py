
from rest_framework import serializers
from rest_framework.exceptions import ValidationError  # Correct import for ValidationError from exceptions
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        author_name = serializers.CharField(source='author.name', read_only=True)

    # Custom validation for publication_year to ensure it's not in the future
    def validate_publication_year(self, value):
        if value > 2025:  # You can replace 2025 with the current year or a dynamic check
            raise serializers.ValidationError("Publication year cannot be in the future.")  # Using 'serializers.ValidationError'
        return value

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # Nested serializer for books

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']


