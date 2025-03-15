from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book

class BookAPITestCase(APITestCase):
    """Test case for the Book API endpoints."""

    def setUp(self):
        """Set up test data."""
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Create an author
        self.author = Author.objects.create(name="J.K. Rowling")

        # Create a book
        self.book = Book.objects.create(title="Harry Potter", publication_year=2001, author=self.author)

        # Define API endpoints
        self.book_list_url = reverse("book-list")
        self.book_detail_url = reverse("book-detail", kwargs={"pk": self.book.id})

        # Authenticate the user
        self.client.login(username="testuser", password="testpass")

    def test_get_book_list(self):
        """Test retrieving the list of books."""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_book(self):
        """Test creating a new book."""
        data = {"title": "New Book", "publication_year": 2023, "author": self.author.id}
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        """Test updating a book."""
        data = {"title": "Updated Title", "publication_year": 2022, "author": self.author.id}
        response = self.client.put(self.book_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    def test_delete_book(self):
        """Test deleting a book."""
        response = self.client.delete(self.book_detail_url)
        response = self.client.delete(f"/api/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
       


    def test_filter_books_by_author(self):
        """Test filtering books by author."""
        response = self.client.get(f"{self.book_list_url}?author={self.author.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_search_books_by_title(self):
        """Test searching books by title."""
        response = self.client.get(f"{self.book_list_url}?search=Harry")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_order_books_by_publication_year(self):
        """Test ordering books by publication year."""
        response = self.client.get(f"{self.book_list_url}?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)