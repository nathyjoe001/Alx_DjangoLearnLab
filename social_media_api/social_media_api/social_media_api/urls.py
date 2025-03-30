from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from posts.views import PostViewSet, CommentViewSet
from accounts.views import UserViewSet  # If you have a User viewset for accounts


schema_view = get_schema_view(
   openapi.Info(
      title="Social Media API",
      default_version='v1',
      description="API documentation for the social media platform",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@socialmedia.local"),
      license=openapi.License(name="MIT"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

# Create a router and register your viewsets
router = DefaultRouter()
router.register(r'posts', PostViewSet)  # Registering the Post viewset
router.register(r'comments', CommentViewSet)  # Registering the Comment viewset
router.register(r'accounts', UserViewSet)  # Registering the User viewset for accounts

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Simplified URL inclusion to include all viewsets
    path('swagger/', schema_view.as_view(), name='swagger'),
]
