from django.contrib import admin
from .models import Book
from .models import CustomUser  # Import CustomUser
from django.contrib.auth.admin import UserAdmin

admin.site.register(Book)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Display columns in list view
    search_fields = ('title', 'author')  # Enable search by title and author
    list_filter = ('publication_year',)  # Add filter by publication year

class CustomUserAdmin(UserAdmin):  # Inherit from UserAdmin
    list_display = ("username", "email", "date_of_birth", "is_staff")
    search_fields = ("username", "email")

    

admin.site.register(CustomUser, CustomUserAdmin)  # Register with admin

