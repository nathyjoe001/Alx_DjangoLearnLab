from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


User = get_user_model()

# Register User
class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login User


class LoginView(generics.GenericAPIView):
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# Follow User
@api_view(['POST'])
#@permissions.IsAuthenticated
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    try:
        user_to_follow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFound(detail="User not found.", code=status.HTTP_404_NOT_FOUND)

    # Add the user to the following list of the currently authenticated user
    request.user.following.add(user_to_follow)
    return Response({"message": "Successfully followed the user!"}, status=status.HTTP_200_OK)

# Unfollow User
@api_view(['POST'])
@permission_classes([IsAuthenticated])
#@permissions.IsAuthenticated
def unfollow_user(request, user_id):
    try:
        user_to_unfollow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFound(detail="User not found.", code=status.HTTP_404_NOT_FOUND)

    # Remove the user from the following list of the currently authenticated user
    request.user.following.remove(user_to_unfollow)
    return Response({"message": "Successfully unfollowed the user!"}, status=status.HTTP_200_OK)

# View all users (used CustomUser.objects.all())
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()  # This will return all users
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
