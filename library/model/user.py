from typing import Optional
from library.model.book import Book, BorrowedBook
from library.model.genre import Genre
from library.persistence.storage import LibraryRepository
from library.model.borrowing import Borrowing



class User:

    email: str
    #borrowed_books: list[BorrowedBook]
    borrowings: list[Borrowing]

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

    def borrow_book(self, book: Book) -> Borrowing:
        borrowing = Borrowing(self, book)
        borrowing.open_borrowing()
        self.borrowings.append(borrowing)
        return borrowing

    def return_books(self, borrowings: list[Borrowing]):
        for borrowing in borrowings:
            borrowing.close_borrowing()

            book: Book = borrowing.get_book()
            #Now do the invoice part



        '''
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
        '''

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

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, User):
            return self.email == other.email
        return NotImplemented

    def __str__(self):
        borrowed_books = "\n".join(str(book) for book in self.borrowed_books)
        read_books = "\n".join(str(book) for book in self.read_books)
        return f"""{self.firstname}, {self.lastname} ({self.email}): {self.country_calling_code}{self.area_code}/{self.landline_number}
            _______BORROWED BOOKS________
            {borrowed_books}
            _______READ BOOKS________
            {read_books}

            Open invoices: {[x.id for x in self.invoices]}
        """
