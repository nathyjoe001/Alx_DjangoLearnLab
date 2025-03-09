from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BookList
from . import views

# Initialize the router
router = DefaultRouter()
# Register the BookViewSet with the router
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Optionally keep the old list view (if you want it)
    path('books/', BookList.as_view(), name='book-list'),  # List books manually (if needed)

    # Include router URLs for CRUD operations on books (automatically handles GET, POST, PUT, DELETE)
    path('api/', include(router.urls)),  # Add the 'api/' prefix for the routes handled by the router
    path('example/', views.example_view, name='example'),
    path('other-endpoint/', views.other_view, name='other_endpoint'),
    
]



