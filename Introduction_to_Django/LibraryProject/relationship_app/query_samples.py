from relationship_app.models import Author, Book, Library, Librarian

# Query 1: Get all books by a specific author
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)
    print(f"Books by {author.name}:")
    for book in books:
        print(f"- {book.title}")

# Query 2: List all books in a library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    print(f"Books in the library {library.name}:")
    for book in books:
        print(f"- {book.title}")

# Query 3: Retrieve the librarian for a specific library
def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    librarian = Librarian.objects.get(library=library)
    print(f"The librarian for {library.name} is {librarian.name}")

# Sample Queries Execution
if __name__ == "__main__":
    # Query books by author
    books_by_author('George Orwell')


    # List all books in a library
    books_in_library('Central Library')

    # Retrieve librarian for a library
    librarian_for_library('Central Library')
