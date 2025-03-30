from django.shortcuts import render

# Create your views here.

from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model





class RegisterView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'token': Token.objects.get(user=user).key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# accounts/views.py


User = get_user_model()

class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Retrieve all users (this line includes CustomUser.objects.all())
        all_users = User.objects.all()

        # Retrieve user to follow by ID provided in the request
        user_to_follow = User.objects.get(id=request.data['user_id'])
        user = request.user

        # Ensure user is not following themselves
        if user == user_to_follow:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the user exists in the database and can be followed
        if user_to_follow not in all_users:
            return Response({"detail": "User to follow does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Add the user_to_follow to the 'following' ManyToMany field of the authenticated user
        user.following.add(user_to_follow)
        user.save()

        return Response({"detail": f"Now following {user_to_follow.username}"}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Retrieve all users (this line includes CustomUser.objects.all())
        all_users = User.objects.all()

        # Retrieve user to unfollow by ID provided in the request
        user_to_unfollow = User.objects.get(id=request.data['user_id'])
        user = request.user

        # Ensure user is not unfollowing themselves
        if user == user_to_unfollow:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the user exists in the database and can be unfollowed
        if user_to_unfollow not in all_users:
            return Response({"detail": "User to unfollow does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Remove the user_to_unfollow from the 'following' ManyToMany field of the authenticated user
        user.following.remove(user_to_unfollow)
        user.save()

        return Response({"detail": f"Unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)
