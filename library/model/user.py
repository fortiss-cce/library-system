from typing import Optional
from library.model.book import Book, BorrowedBook
from library.model.genre import Genre
from library.persistence.storage import LibraryRepository

class User:
    email: str
    read_books: list[Book]
    invoices: list
    firstname: str
    lastname: str
    mobile_number1: str
    country_calling_code: str
    area_code: str
    landline_number: str
    mobile_number2: str
    reading_credits: int = 0

    def __init__(self, email, firstname, lastname, mob1, mob2, area_code, landline, country_code):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.mobile_number1 = mob1
        self.mobile_number2 = mob2
        self.area_code = area_code
        self.landline_number = landline
        self.country_calling_code = country_code
        self.borrowed_books = []
        self.read_books = []
        self.invoices = []

    def borrow_book(self, book: Book) -> Optional[BorrowedBook]:
        try:
            if book.can_borrow():
                borrowed_book = book.borrow_book()
                self.borrowed_books.append(borrowed_book)
                LibraryRepository.update_user(self)
                return borrowed_book
            return None
        except AttributeError:
            return None
        except ValueError:
            return None

    def return_books(self, books: list[BorrowedBook]):
        from library.payment.invoice import Invoice

        invoice: Invoice = Invoice(self)
        for borrowed_book in books:
            if borrowed_book in self.borrowed_books:
                invoice.add_book(borrowed_book)
                self.borrowed_books.remove(borrowed_book)
                book = borrowed_book.return_book()
                self.read_books.append(book)
                LibraryRepository.update_book(book)
        if len(invoice.books) > 0:
            LibraryRepository.create_invoice(invoice)
            self.invoices.append(invoice)
            LibraryRepository.update_user(self)
            return invoice
        else:
            return None

    def get_reading_credits(self, books: list[Book]) -> int:
        reading_credits: int = 0
        for book in books:
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