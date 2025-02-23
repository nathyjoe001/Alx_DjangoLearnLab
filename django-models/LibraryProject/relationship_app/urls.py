
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import views.register  # Import the RegisterView from views.py
from .views import list_books, LibraryDetailView, register



urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

]
