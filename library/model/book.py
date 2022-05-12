from datetime import datetime, timedelta
import json
from library.model.author import Author
from library.model.genre import Genre
from library.model.publisher import Publisher
import xml.etree.ElementTree as et
from abc import abstractmethod

from library.persistence.storage import LibraryRepository


class Book:
    title: str
    authors: list[Author]
    publisher: Publisher
    publication_date: datetime
    genres: list[Genre]
    pages: int
    isbn: str

    def __init__(self, title, authors, publisher, pub_date, genres, pages, isbn, type, duration=0, existing_items=1, borrowed_items=0):
        self.title = title
        self.authors = authors
        self.publisher = publisher
        self.publication_date = pub_date
        self.genres = genres
        self.pages = pages
        self.isbn = isbn

    @classmethod
    def from_borrowed_book(cls, borrowed_book: "BorrowedBook") -> "Book":
        book = Book(
            borrowed_book.book.title,
            borrowed_book.book.authors,
            borrowed_book.book.publisher,
            borrowed_book.book.publication_date,
            borrowed_book.book.genres,
            borrowed_book.book.isbn
        )
        return book

    @abstractmethod
    def can_borrow(self) -> bool:
        raise NotImplementedError("Unspecified book type")

    @abstractmethod
    def get_approximate_duration(self) -> int:
        raise NotImplementedError("Unspecified book type")

    @abstractmethod
    def get_weekly_fee(self) -> int:
        raise NotImplementedError("Unspecified book type")

    def borrow_book(self) -> "BorrowedBook":
        if self.can_borrow():
            LibraryRepository.update_book(self)
            borrowed_book = BorrowedBook.from_book(self)
            borrowed_book.due_date = datetime.now() + timedelta(days=7)
            borrowed_book.current_fee = self.get_weekly_fee()
            return borrowed_book
        raise ValueError("Book cannot be borrowed")

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Book):
            return self.isbn == other.isbn and isinstance(self, type(other))
        elif isinstance(other, BorrowedBook):
            return self.isbn == other.book.isbn and isinstance(self, type(other.book))
        return NotImplemented

    def __str__(self):
        return BookSerializer().serialize(self, "JSON")


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
        self.current_fee += self.book.get_weekly_fee()
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


class ElectronicBook(Book):
    pages: int

    def __init__(self, title, authors, publisher, pub_date, genres, pages, isbn):
        super(ElectronicBook, self).__init__(title, authors, publisher, pub_date, genres, isbn)
        self.pages = pages

    def can_borrow(self) -> bool:
        return True

    def get_approximate_duration(self) -> int:
        return self.pages * 5 * 60

    def get_weekly_fee(self) -> int:
        return 2


class AudioBook(Book):
    duration: int

    def __init__(self, title, authors, publisher, pub_date, genres, isbn, duration=0):
        super(AudioBook, self).__init__(title, authors, publisher, pub_date, genres, isbn)
        self.duration = duration

    def can_borrow(self) -> bool:
        return True

    def get_approximate_duration(self) -> int:
        return self.duration

    def get_weekly_fee(self) -> int:
        return 2


class PaperBook(Book):

    existing_items: int
    borrowed_items: int
    pages: int

    def __init__(self, title, authors, publisher, pub_date, genres, pages, isbn, existing_items=1, borrowed_items=0):
        super().__init__(title, authors, publisher, pub_date, genres, isbn)
        self.pages = pages
        self.existing_items = existing_items
        self.borrowed_items = borrowed_items

    def can_borrow(self) -> bool:
        return self.existing_items - self.borrowed_items > 0

    def get_approximate_duration(self) -> int:
        return self.pages * 3 * 60

    def get_weekly_fee(self) -> int:
        return 5

    def borrow_book(self) -> "BorrowedBook":
        if self.can_borrow():
            self.borrowed_items += 1
        return super().borrow_book()

#    def return_book(self) -> Book:
#        self.borrowed_items -= 1
#        return super().return_book()
