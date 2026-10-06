"""
Exercise: Library Catalog
Module 2 — Advanced Python & Data Handling
Estimated time: 45 minutes

Objective: Build three classes — Book, EBook (inherits from Book), and Catalog —
using OOP principles: encapsulation, inheritance, and method overriding.
"""


# ============================================================
# Book — base class
# ============================================================

class Book:
    """Represents a physical book in the library.

    Physical books can only be checked out by one person at a time,
    so checked_out is a boolean (True/False).
    """

    def __init__(self, title, author, year):
        """Initialize a Book.

        Args:
            title:  Book title string
            author: Author name string
            year:   Publication year (must be a positive integer)

        TODO: Store title, author, year as instance attributes.
              Set self.checked_out = False.
              Validate that year is a positive integer — raise ValueError if not.
        """
        # TODO: implement __init__

        if not isinstance(year, int) or year <= 0:
            raise ValueError("year must be a positive integer")
        
        self.title = title
        self.author = author
        self.year = year
        self.checked_out = False

    def check_out(self):
        """Mark the book as checked out.

        TODO: Set self.checked_out = True.
              Raise ValueError if the book is already checked out.
        """
        # TODO: implement check_out
        
        if self.checked_out:
            raise ValueError("Book is already checked out!")

        self.checked_out = True

    def return_book(self):
        """Return the book to the shelf.

        TODO: Set self.checked_out = False.
              Raise ValueError if the book wasn't checked out.
        """
        # TODO: implement return_book
        
        if not self.checked_out:
            raise ValueError("Book was not checked out!")

        self.checked_out = False

    def __repr__(self):
        """Return a string like: Book('Title', 'Author', year) [available]
        or Book('Title', 'Author', year) [OUT]
        """
        # TODO: implement __repr__

        status = "OUT" if self.checked_out else "available"
        return f"Book('{self.title}', '{self.author}', {self.year}) [{status}]"


# ============================================================
# EBook — subclass of Book
# ============================================================

class EBook(Book):
    """An electronic book. Inherits from Book.

    Why inherit from Book? EBook shares most behaviour (title, author, year,
    catalog methods). Inheritance lets us reuse that and only override what
    genuinely differs.

    Key difference: digital files can be checked out by MULTIPLE users at once,
    so we replace the boolean with an integer counter (_checkout_count).
    """

    def __init__(self, title, author, year, file_size_mb):
        """Initialize an EBook.

        Args:
            title, author, year: same as Book
            file_size_mb: file size as a float (e.g. 15.2)

        TODO: Call super().__init__ to set the Book attributes.
              Store file_size_mb as an attribute.
              Initialize self._checkout_count = 0.

        Note: Book.__init__ sets self.checked_out = False, but EBook uses
        _checkout_count instead. Use a property (see below) to keep things
        compatible with the Catalog.
        """
        # TODO: implement __init__
        
        super().__init__(title, author, year)
        self.file_size_mb = file_size_mb
        self._checkout_count = 0

    @property
    def checked_out(self):
        """Return True if at least one user has this EBook checked out."""
        # TODO: return self._checkout_count > 0
        return self._checkout_count > 0

    @checked_out.setter
    def checked_out(self, value):
        # Book.__init__ tries to set checked_out = False.
        # We intercept that here and do nothing — EBook uses _checkout_count instead.
        pass

    def check_out(self):
        """Increment the checkout counter (multiple users can hold the same EBook).

        TODO: self._checkout_count += 1  (no limit, no error)
        """
        # TODO: implement check_out
        self._checkout_count += 1

    def return_book(self):
        """Decrement the checkout counter.

        TODO: self._checkout_count -= 1
              Raise ValueError if _checkout_count is already 0.
        """
        # TODO: implement return_book
        
        if self._checkout_count == 0:
            raise ValueError("Book is not checked out by anyone!")

        self._checkout_count -= 1

    def __repr__(self):
        """Return a string like:
        EBook('Title', 'Author', year, 15.2 MB) [2 active checkout(s)]
        """
        # TODO: implement __repr__ — include file_size_mb and _checkout_count
        
        return (
            f"EBook('{self.title}', '{self.author}', "
            f"{self.year}, {self.file_size_mb} MB) "
            f"[{self._checkout_count} active checkout(s)]"
        )


# ============================================================
# Catalog — container and search layer
# ============================================================

class Catalog:
    """Holds a collection of Book and EBook objects.

    Design decision: we store books in a plain list (self.books).
    For a production library you'd use a database, but a list is fine
    for this exercise.
    """

    def __init__(self):
        self.books = []   # store your Book and EBook objects here

    def add_book(self, book):
        """Add a Book or EBook to the catalog."""
        self.books.append(book)

    def search_by_author(self, author):
        """Return all books whose author name contains the search string.

        The match should be case-insensitive.
        Returns a list (may be empty).

        TODO: use a list comprehension with .lower() on both sides
        """
        # TODO: implement search_by_author
        
        return [
            book for book in self.books if author.lower() in book.author.lower()
        ]

    def search_by_title(self, keyword):
        """Return all books whose title contains the keyword (case-insensitive, partial match).

        'python' should match 'Python Crash Course'.

        TODO: use a list comprehension with .lower() on both sides
        """
        # TODO: implement search_by_title
        
        return [
            book for book in self.books if keyword.lower() in book.title.lower()
        ]

    def get_available(self):
        """Return all books that are not currently checked out.

        TODO: filter self.books by not b.checked_out
        """
        # TODO: implement get_available
        
        return [
            book for book in self.books if not book.checked_out
        ]

    def summary(self):
        """Print a summary: total books, available, checked out, ebooks.

        TODO: compute counts and print them
        """
        # TODO: implement summary
        total = len(self.books)
        available = len([b for b in self.books if not b.checked_out])
        checked_out = len([b for b in self.books if b.checked_out])
        ebooks = len([b for b in self.books if isinstance(b, EBook)])

        print(f"Total books: {total}")
        print(f"Available: {available}")
        print(f"Checked out: {checked_out}")
        print(f"EBooks: {ebooks}")


# ============================================================
# Tests — run these after implementing all three classes
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Library Catalog — Tests")
    print("=" * 60)

    catalog = Catalog()
    catalog.add_book(Book("Python Crash Course", "Eric Matthes", 2019))
    catalog.add_book(Book("Clean Code", "Robert Martin", 2008))
    catalog.add_book(EBook("AI Engineering", "Chip Huyen", 2025, 15.2))

    results = catalog.search_by_title("python")
    print(f"\nsearch_by_title('python'): {results}")   # should find Python Crash Course

    catalog.books[0].check_out()
    available = catalog.get_available()
    print(f"Available: {len(available) if available is not None else '?'} books")   # should be 2

    catalog.summary()

    # EBook multi-checkout demo
    print("\nEBook multi-checkout demo:")
    ebook = catalog.books[2]
    ebook.check_out()
    ebook.check_out()
    try:
        print(f"  After 2 checkouts: {ebook}")
    except TypeError:
        print("  After 2 checkouts: (implement __repr__ to see output)")
    ebook.return_book()
    try:
        print(f"  After 1 return   : {ebook}")
    except TypeError:
        print("  After 1 return   : (implement __repr__ to see output)")