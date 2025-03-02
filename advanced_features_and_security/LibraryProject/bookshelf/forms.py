from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "published_date", "isbn"]
    
    # Example of input validation
    def clean_isbn(self):
        isbn = self.cleaned_data.get("isbn")
        if len(isbn) != 13:
            raise forms.ValidationError("ISBN must be exactly 13 characters long.")
        return isbn
