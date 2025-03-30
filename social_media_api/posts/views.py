from rest_framework import status, generics, permissions
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view, permission_classes
from notifications.models import Notification
from django.shortcuts import get_object_or_404

User = get_user_model()

# List and Create Posts
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Post Detail View
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

# List and Create Comments
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs['post_id'])
        serializer.save(post=post, author=self.request.user)

# Comment Detail View
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

# Feed View (Posts from followed users)
class UserFeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the list of users the current user is following
        following_users = self.request.user.following.all()

        # Filter posts to show only from users that the current user is following
        return Post.objects.filter(author__in=following_users).order_by('-created_at')  # Ordered by creation date, most recent first


# Like a post
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    # Use get_object_or_404 to fetch the post, returns 404 if not found
    post = get_object_or_404(Post, pk=pk)

    # Prevent the user from liking their own post
    if post.author == request.user:
        return Response({"error": "You cannot like your own post."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the user has already liked the post
    # We use get_or_create to either get the like object or create it if it doesn't exist
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        return Response({"error": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

    # Create a notification for the post author
    Notification.objects.create(
        recipient=post.author,
        actor=request.user,
        verb="liked your post",
        target=post
    )

    return Response({"message": "Post liked successfully!"}, status=status.HTTP_201_CREATED)


# Unlike a post
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    # Use get_object_or_404 to fetch the post, returns 404 if not found
    post = get_object_or_404(Post, pk=pk)

    # Check if the user has liked the post
    like = Like.objects.filter(user=request.user, post=post).first()
    if not like:
        return Response({"error": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

    # Remove the like
    like.delete()

    # Optionally, remove related notifications (like "liked your post") if needed
    notifications = Notification.objects.filter(actor=request.user, verb="liked your post", target=post)
    notifications.delete()

    return Response({"message": "Post unliked successfully!"}, status=status.HTTP_200_OK)
