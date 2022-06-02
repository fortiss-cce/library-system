from datetime import datetime, timedelta
from multiprocessing.sharedctypes import Value

from matplotlib.style import library
from library.model.book import Book, AudioBook, ElectronicBook, PaperBook, Genre
from library.model.user import User
from tests.test_user_borrow_book import borrow_book

class LibraryBookListing:
    book: Book
    existing_items: int
    borrowed_items: int

    def __init__(self, book: Book):
        self.book = book
        self.existing_items = 1
        self.borrowed_items = 0

    @property
    def book(self) -> Book:
        return self.book

    def can_be_borrowed(self) -> bool:
        if self.book.is_digital():
            return True
        else:
            return self.existing_items - self.borrowed_items > 0

    def get_weekly_fee(self) -> int:
        if isinstance(self.book, PaperBook):
            return 5
        elif isinstance(self.book, ElectronicBook):
            return 2
        elif isinstance(self.book, AudioBook):
            return 2
        else:
            raise AttributeError("No such book type...")

class BorrowedLibraryBook:
    borrowed_by: User
    listing: LibraryBookListing
    due_date: datetime
    current_fee: float
    was_returned: bool

    def __init__(self, borrowed_by: User, listing: LibraryBookListing, due_date: datetime, current_fee: float):
        self.borrowed_by = borrowed_by
        self.listing = listing
        self.due_date = due_date
        self.current_fee = current_fee
        self.was_returned = False

class LibraryAccount:
    user: User
    borrowed_books: list[BorrowedLibraryBook]
    pending_payment: list[BorrowedLibraryBook]
    read_books: list[Book]
    reading_credits: int

    def __init__(self, user: User):
        self.user = user
        self.borrow_books = []
        self.pending_payment = []
        self.read_books = []

class LibraryAccountInvoice:
    user: User
    borrows: list[BorrowedLibraryBook]
    fee: float

    def __init__(self, user: User, borrows: list[BorrowedLibraryBook], fee: float):
        self.user = user
        self.borrows = borrows
        self.fee = fee

class Library:
    accounts: dict[str, LibraryAccount]
    books: dict[str, LibraryBookListing]

    def __init__(self):
        self.books = {}

    def create_listing(self, book: Book):
        if book.isbn not in self.books:
            self.books[book.isbn] = LibraryBookListing(book)
        else:
            self.books[book.isbn].existing_items += 1

    def renew_rental(self, book: BorrowedLibraryBook):
        book.due_date += timedelta(days=7)
        book.current_fee += book.listing.get_weekly_fee()
        return self

    def return_book(self, borrowed: BorrowedLibraryBook):
        if borrowed.was_returned:
            raise ValueError("book was already returned")
        if borrowed.listing.book_type == "Paper":
            self.borrowed_items -= 1
        account = self.accounts[borrowed.borrowed_by.email]
        account.read_books.append(borrowed.listing.book)
        account.pending_payment.append(borrowed)
        account.borrowed_books.remove(borrowed)
        borrowed.was_returned = True

    def borrow_book(self, listing: LibraryBookListing, user: User):
        if not user.email in self.accounts:
            raise ValueError("Unknown user")
        if not listing.can_be_borrowed():
            raise ValueError("Book cannot be borrowed")
        if listing.book_type == "Paper":
            listing.borrowed_items += 1
        due_date = datetime.now() + timedelta(days=7)
        current_fee = self.get_weekly_fee()
        return BorrowedLibraryBook(user, listing, due_date, current_fee)

    @staticmethod
    def compute_reading_credits(borrows: list[BorrowedLibraryBook]) -> int:
        reading_credits: int = 0
        for borrow in borrows:
            book = borrow.listing.book
            for genre in book.genres:
                if genre == Genre.HISTORY:
                    reading_credits += 1
                elif genre == Genre.MEDICINE:
                    reading_credits += 2
                elif genre == Genre.SOCIOLOGY:
                    reading_credits += 2
                else:
                    reading_credits += 0
        return reading_credits

    def create_invoice_for_user(self, user: User) -> LibraryAccountInvoice:
        if not user.email in self.accounts:
            raise ValueError("Unknown user")
        account = self.accounts[user.email]

        price_per_book: float = 3.55
        min_books_for_discount: int = 3
        discount_per_book: float = 0.5
        discount_per_reading_credit: float = 0.5
        current_reading_credits = account.reading_credits

        pending_payment = account.pending_payment
        reading_credits: int = Library.compute_reading_credits(pending_payment)
        price: float = len(pending_payment) * price_per_book
        for pending in pending_payment:
            price += pending.current_fee
        discount_count: int = max(0, len(self.books) - min_books_for_discount)
        discount: float = discount_count * discount_per_book
        discount += current_reading_credits * discount_per_reading_credit
        return (
            round(price - discount if price - discount > 0.0 else 0.0, 2),
            reading_credits,
        )