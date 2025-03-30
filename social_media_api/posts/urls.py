from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from . import views

# Initialize the router
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

# Define the additional routes for liking/unliking and user feed
urlpatterns = [
    # URLs for liking and unliking posts
    path('posts/<int:pk>/like/', views.like_post, name='like-post'),
    path('posts/<int:pk>/unlike/', views.unlike_post, name='unlike-post'),

    # Feed URL (Post from followed users)
    path('feed/', views.UserFeedView.as_view(), name='user-feed'),

    # Add router URLs to urlpatterns
] + router.urls
