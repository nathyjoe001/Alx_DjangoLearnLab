from django.urls import path
from .views import RegisterView, LoginView
from .views import FollowUserView, UnfollowUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('follow/', FollowUserView.as_view(), name='follow'),
    path('unfollow/', UnfollowUserView.as_view(), name='unfollow'),
]
