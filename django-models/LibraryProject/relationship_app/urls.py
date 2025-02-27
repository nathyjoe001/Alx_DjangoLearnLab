
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Import the RegisterView from views.py
from .views import list_books, LibraryDetailView, register
from .views import add_book, edit_book, delete_book, book_list
from .views import admin_view, librarian_view, member_view



urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),

    path('', book_list, name='book_list'),  # View for listing books
    path('add_book/', add_book, name='add_book'),  # View for adding a book
    path('edit_book/<int:book_id>/', edit_book, name='edit_book'),  # View for editing a book
    path('delete_book/<int:book_id>/', delete_book, name='delete_book'),  # View for deleting a book
]
