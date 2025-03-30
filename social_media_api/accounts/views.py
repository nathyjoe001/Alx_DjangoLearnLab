from rest_framework import status, views, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import NotFound
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer

User = get_user_model()

# Register User
class RegisterView(views.APIView):
    def post(self, request):
        # Initialize the User serializer with the data sent in the request
        serializer = UserSerializer(data=request.data)
        
        # Validate the data and create the user
        if serializer.is_valid():
            user = serializer.save()
            # Create the authentication token for the new user
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        
        # If the serializer is invalid, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login User
class LoginView(views.APIView):
    def post(self, request):
        # Get the username and password from the request
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user:
            # If user is authenticated, create or retrieve a token
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        
        # If the credentials are invalid, return an error message
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# Follow User
@api_view(['POST'])
def follow_user(request, user_id):
    try:
        # Try to get the user to follow
        user_to_follow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFound(detail="User not found.", code=status.HTTP_404_NOT_FOUND)

    # Add the user to the following list of the currently authenticated user
    request.user.following.add(user_to_follow)
    return Response({"message": "Successfully followed the user!"}, status=status.HTTP_200_OK)

# Unfollow User
@api_view(['POST'])
def unfollow_user(request, user_id):
    try:
        # Try to get the user to unfollow
        user_to_unfollow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFound(detail="User not found.", code=status.HTTP_404_NOT_FOUND)

    # Remove the user from the following list of the currently authenticated user
    request.user.following.remove(user_to_unfollow)
    return Response({"message": "Successfully unfollowed the user!"}, status=status.HTTP_200_OK)
