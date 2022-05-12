from datetime import datetime, timedelta
import json
from library.model.author import Author
from library.model.genre import Genre
from library.model.publisher import Publisher
import xml.etree.ElementTree as et

from library.persistence.storage import LibraryRepository

from dataclasses import dataclass
from enum import Enum

class BookType(Enum):
    PAPER = 1
    ELECTRONIC = 2
    AUDIO = 2

@dataclass(kw_only=True)
class Book:
    title: str
    authors: list[Author]
    publisher: Publisher
    publication_date: datetime
    genres: list[Genre]
    pages: int
    isbn: str
    book_type: BookType
    duration: Optional[int] = None

    def __post_init__(self):
        assert self.duration is not None

    def get_approximate_duration(self) -> int:
        if self.book_type == BookType.PAPER:
            return self.pages * 3 * 60
        elif self.book_type == BookType.ELECTRONIC:
            return self.pages * 5 * 60
        elif self.book_type == BookType.Audio:
            return self.duration
        else:
            raise AttributeError("No such book type...")

    def get_weekly_fee(self) -> int:
        if self.book_type == BookType.PAPER:
            return 5
        elif self.book_type == BookType.ELECTRONIC:
            return 2
        elif self.book_type == BookType.Audio:
            return 2
        else:
            raise AttributeError("No such book type...")

    # TODO Move
    def borrow_book(self) -> BorrowedBook:
        if self.can_borrow():
            if self.book_type == BookType.PAPER:
                self.borrowed_items += 1
            LibraryRepository.update_book(self)
            borrowed_book = BorrowedBook.from_book(self)
            borrowed_book.due_date = datetime.now() + timedelta(days=7)
            borrowed_book.current_fee = self.get_weekly_fee()
            return borrowed_book
        raise ValueError("Book cannot be borrowed")

    def __str__(self):
        return self.serialize_json()

    def serialize_json(self):
        book_info = {
            "id": self.isbn,
            "title": self.title,
            "authors": [author.get_fullname() for author in self.authors],
            "available_items": self.existing_items - self.borrowed_items,
            "borrowed_items": self.borrowed_items,
        }
        return json.dumps(book_info)
    
    def serialize_xml(self):
        book_info = et.Element("book", attrib={"id": self.isbn})
        title = et.SubElement(book_info, "title")
        title.text = self.title
        authors = et.SubElement(book_info, "authors")
        authors.text = ", ".join([author.get_fullname() for author in self.authors])
        avail = et.SubElement(book_info, "available")
        avail.text = str(self.existing_items - self.borrowed_items)
        authors = et.SubElement(book_info, "borrowed")
        authors.text = str(self.borrowed_items)
        return et.tostring(book_info, encoding="Unicode")

@dataclass
class BookBorrowed:
    book: Book
    due_date: datetime
    current_fee: float

    def extend_rental(self, weeks: int = 1):
        assert weeks >= 0
        self.due_date += timedelta(weeks = weeks)
        self.current_fee += self.get_weekly_fee() * weeks


