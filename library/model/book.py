from datetime import datetime, timedelta
import json
from library.model.author import Author
from library.model.genre import Genre
from library.model.publisher import Publisher
from library.model.borrowing import Borrowing
import xml.etree.ElementTree as et

from library.persistence.storage import LibraryRepository


class Book:
    title: str
    authors: list[Author]
    publisher: Publisher
    publication_date: datetime
    genres: list[Genre]
    pages: int
    isbn: str

    existing_items: int
    borrowed_items: int

    book_type: str
    duration: int = 0

    def __init__(self, title, authors, publisher, pub_date, genres, pages, isbn, type, duration=0, existing_items=1, borrowed_items=0):
        self.title = title
        self.authors = authors
        self.publisher = publisher
        self.publication_date = pub_date
        self.genres = genres
        self.pages = pages
        self.isbn = isbn
        self.book_type = type
        self.duration = duration
        self.existing_items = existing_items
        self.borrowed_items = borrowed_items

    def can_borrow(self) -> bool:
        if self._book_type == "Paper":
            return self.existing_items - self.borrowed_items > 0
        elif self._book_type == "Electronic":
            return True
        elif self._book_type == "Audio":
            return True
        else:
            raise AttributeError("No such book type...")

    def get_approximate_duration(self) -> int:
        if self._book_type == "Paper":
            return self.pages * 3 * 60
        elif self._book_type == "Electronic":
            return self.pages * 5 * 60
        elif self._book_type == "Audio":
            return self.duration
        else:
            raise AttributeError("No such book type...")


    def get_weekly_fee(self) -> int:
        if self._book_type == "Paper":
            return 5
        elif self._book_type == "Electronic":
            return 2
        elif self._book_type == "Audio":
            return 2
        else:
            raise AttributeError("No such book type...")

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Book) or isinstance(other, BorrowedBook):
            return self.isbn == other.isbn and self._book_type == other._book_type
        return NotImplemented

    def __str__(self):
        return BookSerializer().serialize(self, "JSON")

'''
class BorrowedBook(Book):
    due_date: datetime
    current_fee: float

    @classmethod
    def from_book(cls, book: Book) -> "BorrowedBook":
        borrowed_book = BorrowedBook(
            book.title,
            book.authors,
            book.publisher,
            book.publication_date,
            book.genres,
            book.pages,
            book.isbn,
            book._book_type,
            book.duration,
            book.existing_items,
            book.borrowed_items,
        )
        return borrowed_book

    def renew_rental(self) -> "BorrowedBook":
        self.due_date += timedelta(days=7)
        self.current_fee += self.get_weekly_fee()
        return self

    def return_book(self) -> Book:
        if self._book_type == "Paper":
            self.borrowed_items -= 1
        book = Book.from_borrowed_book(self)
        LibraryRepository.update_book(book)
        return book

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Book) or isinstance(other, BorrowedBook):
            return self.isbn == other.isbn and self._book_type == other._book_type
        return NotImplemented
'''

class BookSerializer:
    def serialize(self, book: Book, format: str):
        if format == "JSON":
            book_info = {
                "id": book.isbn,
                "title": book.title,
                "authors": [author.get_fullname() for author in book.authors],
                "available_items": book.existing_items - book.borrowed_items,
                "borrowed_items": book.borrowed_items,
            }
            return json.dumps(book_info)
        elif format == "XML":
            book_info = et.Element("book", attrib={"id": book.isbn})
            title = et.SubElement(book_info, "title")
            title.text = book.title
            authors = et.SubElement(book_info, "authors")
            authors.text = ", ".join([author.get_fullname() for author in book.authors])
            avail = et.SubElement(book_info, "available")
            avail.text = str(book.existing_items - book.borrowed_items)
            authors = et.SubElement(book_info, "borrowed")
            authors.text = str(book.borrowed_items)
            return et.tostring(book_info, encoding="Unicode")
        else:
            raise ValueError(format)
