
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
#from django.shortcuts import get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm

from django.db.models import Q
from django.shortcuts import render
from .models import Post
from taggit.models import Tag


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/post_detail.html', {'post': post})


# View to display posts that belong to a specific tag
def posts_by_tag(request, tag_name):
    # Get the tag using django-taggit's Tag model
    tag = get_object_or_404(Tag, name=tag_name)
    
    # Use filter to get posts with the specified tag
    posts = Post.objects.filter(tags__name=tag_name)  # 'tags__name' is the key to filter by tag name
    
    return render(request, 'blog/posts_by_tag.html', {'posts': posts, 'tag': tag})




def search_posts(request):
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    else:
        posts = Post.objects.all()

    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})




# Create your views here.


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})

# Register view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# views.py

# List view to show all blog posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

# Detail view to show a single post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

# Create view for authenticated users to create a post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author as the logged-in user
        return super().form_valid(form)

# Update view for authenticated users to edit their own posts
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Delete view for authenticated users to delete their own posts
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    


# View for adding a comment
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.kwargs['post_id']})

# View for editing a comment
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})

# View for deleting a comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})
    


# View for creating a new comment
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user  # Set the author of the comment to the logged-in user
            comment.post = post  # Associate the comment with the post
            comment.save()  # Save the comment
            return redirect('post_detail', pk=post.id)  # Redirect to the post detail page (ensure this URL exists)
    else:
        form = CommentForm()

    return render(request, 'blog/comment_form.html', {'form': form, 'post': post})

def update_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()  # Save the updated comment
            return redirect('post_detail', pk=comment.post.id)  # Redirect to the post detail page
    else:
        form = CommentForm(instance=comment)  # Pre-fill the form with the current comment content

    return render(request, 'blog/comment_form.html', {'form': form, 'comment': comment})