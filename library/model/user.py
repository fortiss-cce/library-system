from typing import NamedTuple
from library.model.book import Book, BookBorrowed
from library.model.reading_creadits import ReadingCreditsPerGenre
from library.payment.invoice import Invoice
from library.persistence.storage import LibraryRepository


class PersonalData(NamedTuple):
    email: str
    firstname: str
    lastname: str
    mobile_number1: str = ''  # Including country code
    mobile_number2: str = ''  # Including country code
    landline_number: str = ''  # Including country code and area code

    def __str__(self):
        """Prints name, email and (if available), the full landline number"""
        if len(self.landline_number) > 0:
            return f'{self.firstname}, {self.lastname} ({self.email}): {self.landline_number}'
        else:
            return f'{self.firstname}, {self.lastname} ({self.email})'


class User:

    personal_data: PersonalData
    borrowed_books: list[BookBorrowed]
    read_books: list[Book]
    invoices: list[Invoice]
    reading_credits: int

    def __init__(self, personal_data: PersonalData):
        self.personal_data = personal_data
        self.borrowed_books = []
        self.read_books = []
        self.invoices = []

    def borrow_book(self, books: list[Book]) -> None:
        for book in books:
            if not book.can_borrow():
                raise ValueError("Book is not available")
            borrowed_book = book.borrow_book()
            self.borrowed_books.append(borrowed_book)
            LibraryRepository.borrow_book(book)

    def return_book(self, books: list[BookBorrowed]) -> Invoice:
        if not all(book in self.borrowed_books for book in books):
            raise ValueError("At least one book from the list is not borrowed and so cannot be returned")
        invoice: Invoice = Invoice(self)
        if not books:
            return invoice

        for borrowed_book in books:
            invoice.add_book(borrowed_book)
            self.borrowed_books.remove(borrowed_book)
            book = borrowed_book.return_book()
            self.read_books.append(book)
            LibraryRepository.return_book(book)
        LibraryRepository.create_invoice(invoice)
        self.invoices.append(invoice)
        LibraryRepository.update_user(self)
        return invoice

    @property
    def email(self) -> str:
        return self.personal_data.email

    @property
    def firstname(self) -> str:
        return self.personal_data.firstname

    @property
    def lastname(self) -> str:
        return self.personal_data.lastname

    @property
    def reading_credits(self) -> int:
        """
        Changed functionality of that method (was get_reading_credits):
        -> now it returns the number of reading credits for the users read books
        -> previously, it returned the reading credits for a list of given books, which was not dependent on the user
        """
        return sum(ReadingCreditsPerGenre[genre] for book in self.read_books for genre in book.genres)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, User):
            return self.email == other.email
        return NotImplemented

    def __str__(self):
        borrowed_books = "\n".join(str(book) for book in self.borrowed_books)
        read_books = "\n".join(str(book) for book in self.read_books)
        return f"""{self.personal_data}
            _______BORROWED BOOKS________
            {borrowed_books}
            _______READ BOOKS________
            {read_books}

            Open invoices: {[x.id for x in self.invoices]}
        """
