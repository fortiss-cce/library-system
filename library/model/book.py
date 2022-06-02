from datetime import datetime, timedelta
import json
from library.model.author import Author
from library.model.genre import Genre
from library.model.publisher import Publisher
import xml.etree.ElementTree as et

from library.persistence.storage import LibraryRepository

class Book:
    isbn: str
    title: str
    authors: list[Author]
    publisher: Publisher
    publication_date: datetime
    genres: list[Genre]
    pages: int

    def __init__(self, title, authors, publisher, pub_date, genres, pages, isbn):
        self.isbn = isbn
        self.title = title
        self.authors = authors
        self.publisher = publisher
        self.publication_date = pub_date
        self.genres = genres
        self.pages = pages

    @property
    def book_type(self) -> str:
        return self._book_type
    def get_approximate_duration(self) -> int:
        return 0
    def is_digital() -> bool:
        return True

class AudioBook(Book):
    _duration: int

    def __init__(self, title, authors, publisher, pub_date, genres, pages, isbn, duration = 0.0):
        super().__init__(title, authors, publisher, pub_date, genres, pages, isbn)
        self._duration = duration

    def get_approximate_duration(self) -> int:
        return self.duration
    def is_digital() -> bool:
        True


class ElectronicBook(Book):
    def __init__(self, title, authors, publisher, pub_date, genres, pages, isbn):
        super().__init__(title, authors, publisher, pub_date, genres, pages, isbn)

    def get_approximate_duration(self) -> int:
        return self.pages * 5 * 60
    def is_digital() -> bool:
        True

class PaperBook(Book):
    def __init__(self, title, authors, publisher, pub_date, genres, pages, isbn):
        super().__init__(title, authors, publisher, pub_date, genres, pages, isbn)

    def get_approximate_duration(self) -> int:
        return self.pages * 3 * 60
    def is_digital() -> bool:
        False