import logging
from typing import Optional
from library.model.book import Book, BorrowedBook
from library.model.genre import Genre
# from library.payment.invoice import Invoice # Future issue, remove circular loop 
# from library.payment.invoice import Invoice
from library.persistence.storage import LibraryRepository


class User:
    """ Class for library user. """

    email: str
    borrowed_books: list[BorrowedBook]
    read_books: list[Book]
    invoices: list
    firstname: str
    lastname: str
    mobile_number1: str # Merge with mobile number 2? 
    country_calling_code: str
    area_code: str
    landline_number: str
    mobile_number2: str
    reading_credits: int = 0

    def __init__(self, email, firstname, lastname, mob_nbr_1, mob_nbr_2, area_code, landline, country_code):
        self.email = email
        self.firstname, self.lastname = firstname, lastname
        self.mobile_number1, self.mobile_number2 = mob_nbr_1, mob_nbr_2
        self.landline_number, self.country_calling_code = landline, country_code
        self.area_code = area_code
        self.borrowed_books, self.read_books, self.invoices = [], [], []

    def borrow_book(self, book: Book) -> Optional[BorrowedBook]:
        """ Function that tries to borrow a specific book. """

        try:
            if book.can_borrow(): # Can raise AttributeError
                borrowed_book = book.borrow_book() # Potential valueError
                self.borrowed_books.append(borrowed_book)
                LibraryRepository.update_user(self)
                return borrowed_book
        except (ValueError, AttributeError) as e:
            print(e)

    def return_books(self, books: list[BorrowedBook]):
        """ Return books, get invoice to process further. """

        from library.payment.invoice import Invoice

        invoice: Invoice = Invoice(self)
        for borrowed_book in books: 
            if borrowed_book in self.borrowed_books: # Shouldn't be necessary ... 
                invoice.add_book(borrowed_book)
                self.update_library(borrowed_book = borrowed_book)
        
        self._set_current_invoice(invoice = invoice)

    def _set_current_invoice(self, invoice): # This can probably be done different ... 
        """ Set the current invoice for user. """
        
        if len(invoice.books) > 0:
            LibraryRepository.create_invoice(invoice)
            self.invoices.append(invoice)
            LibraryRepository.update_user(self)

        self._current_invoice = invoice

    def _get_invoices(self):
        """ Get invoice if there are any returned books. """
        return self.invoices

    def _get_current_invoice(self):
        return self._current_invoice

    def update_library(self, borrowed_book) -> None: 
        """ Update borrowed book and read book lists. """

        self.borrowed_books.remove(borrowed_book)
        book = borrowed_book.return_book()
        self.read_books.append(book)
        LibraryRepository.update_book(book)

    def get_reading_credits(self, books: list[Book]) -> int: # Could be done as a dictionary 
        reading_credits: int = 0
        for book in books:
            for genre in book.genres:
                if genre == Genre.HISTORY:
                    reading_credits += 1
                elif genre == Genre.MEDICINE:
                    reading_credits += 2
                elif genre == Genre.SOCIOLOGY:
                    reading_credits += 2
                else: # This can be removed 
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
