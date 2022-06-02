from datetime import datetime, timedelta
import json
from typing import Union
from abc import abstractmethod
from library.model.author import Author
from library.model.genre import Genre
from library.model.publisher import Publisher
import xml.etree.ElementTree as et

from library.persistence.storage import LibraryRepository

class BookSerialNumber:
    title: str
    authors: list[Author]
    publisher: Publisher
    publication_date: datetime
    genres: list[Genre]
    pages: int
    isbn: str

    existing_items: int
    borrowed_items: int

    _book_type: Union["PaperType", "ElectronicType", "AudioType"]
    duration: int = 0
    _renew_rental_data: int = 7

    existing_books_list: List[Book]
    in_stock_list: List[Book]
    borrowed_books_list: List[Book]

   

    def __init__(self, title, authors, publisher, pub_date, genres, pages, isbn, book_type, duration=0, existing_items=1, borrowed_items=0):
        self.title = title
        self.authors = authors
        self.publisher = publisher
        self.publication_date = pub_date
        self.genres = genres
        self.pages = pages
        self.isbn = isbn

        self.set_book_type(book_type)

        self.duration = duration
        self.existing_items = existing_items

        self.borrowed_items = borrowed_items
        self.in_stock_items = self.existing_items - self.borrowed_items

    def init_existing_books(self):
        self.existing_books_list = [Book(is_borrowed = False)] * self.existing_items + [Book(is_borrowed = True)] * self.borrowed_items
    def get_borrowed_books(self): -> List[Book]
        return [book for book in self.existing_books_list if book.is_borrowed]
    def get_in_stock_books(self): -> List[Book]
        return [book for book in self.existing_books_list if not book.is_borrowed ]

    def set_book_type(self, book_type) -> None:
        if book_type == "Paper":
            self._book_type = PaperType()
        elif book_type == "Electronic":
            self._book_type = ElectronicType()
        elif book_type == "Audio":
            self._book_type = AudioType()
        else:
            raise AttributeError("No such book type...")
        print("Book successfully set")


    def can_borrow(self) -> bool:
        return self._book_type.can_borrow(self) and len(self.in_stock_list) > 0 
       
    def get_approximate_duration(self) -> int:
        return self._book_type.get_approximate_duration(self) 
     
    def get_weekly_fee(self) -> int:
        return self._book_type.get_weekly_fees()

    def check_books_stock_consistency(self):
        assert len(self.borrowed_books_list) + self.in_stock_list)== self.existing_items, "Stock not consistent!!!"

    def borrow_book(self) -> "BorrowedBook":

        if self.can_borrow(): 
            LibraryRepository.update_book(self)
            borrowed_book = self.get_in_stock_books()[0]
            borrowed_book.set_due_time(datetime.now() + timedelta(days=self._renew_rental_data))
            borrowed_book.set_current_fee(self.get_weekly_fee())
            borrowed_book.borrow_book()
            self.check_books_stock_consistency()
            return borrowed_book
        raise ValueError("Book cannot be borrowed")

    def __str__(self):
        return BookSerializer().serialize(self, "JSON")



class Book():
    due_date: datetime
    current_fee: float
    _is_borrowed: bool
    def __init__(self, is_borrowed: bool)
  
    def renew_rental(self) -> "BorrowedBook":
        self.due_date += timedelta(days=self._renew_rental_data)
        self.current_fee += self.get_weekly_fee()
        return self
    def set_current_fee(self, current_fee): 
        self.current_fee = current_fee
    
    def borrowed_book(self):
        self._is_borrowed = False


    def return_book(self) -> Book:
        if self._book_type.book_type == "Paper":
            self.borrowed_items -= 1
        book = Book.from_borrowed_book(self)
        LibraryRepository.update_book(book)
        self._is_borrowed = False
        return book

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

class BookType():
    book_type: str 
    weekly_fees: int
    @abstractmethod
    def can_borrow(self, book: Book):
        pass

    @abstractmethod
    def get_approximate_duration(self, book: Book):
        pass
    
    def get_weekly_fees(self):
        return self.weekly_fees

class PaperType(BookType):
    book_type: str = "paper"
    weekly_fees: int = 5
    page_factor:  int = 180
    def can_borrow(self, book: Book):
        return book.existing_items - book.borrowed_items > 0 
    def get_approximate_duration(self, book: Book):
        return book.pages * self.pages_factor
        
class ElectronicType(BookType):
    book_type: str = "Electronic"
    weekly_fees: int = 2
    page_factor: int = 300
    def can_borrow(self, book: Book):
        return True
    def get_approximate_duration(self, book: Book):
        return book.pages * self.pages_factor
        
class AudioType(BookType):
    book_type: str = "Audio"
    weekly_fees: int = 2
    
    def can_borrow(self, book: Book):
        return True
    def get_approximate_duration(self, book: Book):
        return book.duration
        

