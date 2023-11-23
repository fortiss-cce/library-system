from datetime import datetime, timedelta
import json
from library.model.author import Author
from library.model.genre import Genre
from library.model.publisher import Publisher
import xml.etree.ElementTree as et

from library.persistence.storage import LibraryRepository
from abc import ABCMeta, abstractmethod

class Book(object, metaclass=ABCMeta):
    title: str
    authors: list[Author]
    publisher: Publisher
    publication_date: datetime
    genres: list[Genre]
    isbn: str

    @abstractmethod
    def __init__(self, title, authors, publisher, pub_date, genres, isbn):
        self.title = title
        self.authors = authors
        self.publisher = publisher
        self.publication_date = pub_date
        self.genres = genres
        self.isbn = isbn

    @abstractmethod
    def can_borrow(self) -> bool:
        pass

    @abstractmethod
    def get_approximate_duration(self) -> int:
        pass

    @abstractmethod
    def get_weekly_fee(self) -> int:
        pass

    @abstractmethod
    def borrow_book(self) -> "BorrowedBook":
        pass

    def _create_book_borrow(self) -> "BorrowedBook":
        LibraryRepository.update_book(self)
        borrowed_book = BorrowedBook(self)
        return borrowed_book

    @abstractmethod
    def return_book(self):
        pass

    def _handle_book_return(self):
        LibraryRepository.update_book(self)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Book) or isinstance(other, BorrowedBook):
            return self.isbn == other.isbn and (type(self) is type(other))
        return NotImplemented

    def __str__(self):
        return BookSerializer.serialize(self, "JSON")

class AudioBook(Book):
    duration: int = 0

    def __init__(self, title, authors, publisher, pub_date, genres, isbn, duration):
        Book.__init__(self, title, authors, publisher, pub_date, genres, isbn)
        self.duration = duration

    def can_borrow(self) -> bool:
        return True

    def borrow_book(self) -> "BorrowedBook":
        if self.can_borrow():
            return self._create_book_borrow()
        raise ValueError("Book cannot be borrowed")

    def return_book(self):
        self._handle_book_return(self)

    def get_approximate_duration(self) -> int:
        return self.duration

    def get_weekly_fee(self) -> int:
        return 2

class ElectronicBook(Book):
    pages: int

    def __init__(self, title, authors, publisher, pub_date, genres, isbn, pages):
        Book.__init__(self, title, authors, publisher, pub_date, genres, isbn)
        self.pages = pages
    def can_borrow(self) -> bool:
        return True

    def borrow_book(self) -> "BorrowedBook":
        if self.can_borrow():
            return self._create_book_borrow()
        raise ValueError("Book cannot be borrowed")

    def return_book(self):
        self._handle_book_return(self)

    def get_approximate_duration(self) -> int:
        return self.pages * 5 * 60

    def get_weekly_fee(self) -> int:
        return 2

class PaperBook(Book):
    pages: int
    existing_items: int
    borrowed_items: int

    def __init__(self, title, authors, publisher, pub_date, genres, isbn, pages, existing_items, borrowed_items):
        Book.__init__(self, title, authors, publisher, pub_date, genres, isbn)
        self.pages = pages
        self.existing_items = existing_items
        self.borrowed_items = borrowed_items

    def can_borrow(self) -> bool:
        return self.existing_items - self.borrowed_items > 0

    def borrow_book(self) -> "BorrowedBook":
        if self.can_borrow():
            self.borrowed_items += 1
            return self._create_book_borrow()
        raise ValueError("Book cannot be borrowed")

    def return_book(self):
        self.borrowed_items -= 1
        self._handle_book_return(self)

    def get_approximate_duration(self) -> int:
        return self.pages * 3 * 60

    def get_weekly_fee(self) -> int:
        return 5


class BorrowedBook():
    book: Book
    due_date: datetime
    current_fee: float
    is_returned: bool

    def __init__(self, book):
        self.book = book
        self.due_date = datetime.now() + timedelta(days=7)
        self.current_fee = book.get_weekly_fee()
        self.is_returned = False

    def renew_rental(self):
        self.due_date += timedelta(days=7)
        self.current_fee += self.get_weekly_fee()

    def return_book(self) -> Book:
        if not self.is_returned:
            self.book.return_book()
            self.is_returned = False
        else:
            raise ValueError("Book has already been returned")

    def __eq__(self, other):
        """Overrides the default implementation"""
        return self.book.__eq__(other.book)


class BookSerializer:

    @staticmethod
    def serialize(book: Book, format: str):
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
