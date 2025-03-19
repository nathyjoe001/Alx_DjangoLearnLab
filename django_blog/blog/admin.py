from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Post  # Import the Post model

# Define a custom admin class to customize how the Post model is displayed
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')  # Customize the list view

# Register the Post model with the custom admin class
admin.site.register(Post, PostAdmin)



