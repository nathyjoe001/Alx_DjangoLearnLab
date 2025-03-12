from rest_framework import serializers
from .models import Author, Book

# BookSerializer should inherit from serializers.ModelSerializer
class BookSerializer(serializers.ModelSerializer):
    # Meta class to link this serializer to the Book model
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    # Custom validation method to ensure publication_year is not in the future
    def validate_publication_year(self, value):
        # Import ValidationError
        from rest_framework.exceptions import ValidationError

        # Custom validation for the publication year
        if value > 2025:  # Replace 2025 with the current year or dynamic check
            raise ValidationError("Publication year cannot be in the future.")
        return value

# AuthorSerializer to include nested BookSerializer
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # Nested BookSerializer

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

