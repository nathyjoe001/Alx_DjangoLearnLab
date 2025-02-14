book.delete()

# Confirm deletion
books = Book.objects.all()
print(books)

# Expected outcome

[]
