from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from library.model.book import Book
    from library.model.user import User
    from library.model.author import Author
    from library.model.publisher import Publisher
    from library.payment.invoice import Invoice

users: list[User] = []
books: list[Book] = []
books_borrowed: list[Book] = []
authors: list[Author] = []
publishers: list[Publisher] = []
invoices: list[Invoice] = []


class LibraryRepository:
    @staticmethod
    def read_users() -> list[User]:
        return users

    @staticmethod
    def read_books() -> list[Book]:
        return books

    @staticmethod
    def read_authors() -> list[Author]:
        return authors

    @staticmethod
    def read_publishers() -> list[Publisher]:
        return publishers

    @staticmethod
    def read_invoices() -> list[Invoice]:
        return invoices

    # books
    @staticmethod
    def create_book(book: Book):
        books.append(book)

    @staticmethod
    def read_book(isbn: str) -> Optional[Book]:
        found_books = [x for x in books if x.isbn == isbn]
        if len(found_books) > 0:
            return found_books[0]
        return None

    @staticmethod
    def update_book(book: Book):
        index = books.index(book)
        if index >= 0:
            books[index] = book

    @staticmethod
    def delete_book(book: Book):
        index = books.index(book)
        if index >= 0:
            books.remove(book)

    @staticmethod
    def borrow_book(book: Book):
        books.remove(book)
        books_borrowed.append(book)

    @staticmethod
    def return_book(book: Book):
        books_borrowed.remove(book)
        books.append(book)

        
    # users
    @staticmethod
    def create_user(user: User):
        users.append(user)

    @staticmethod
    def read_user(email: str) -> Optional[User]:
        found_users = [x for x in users if x.email == email]
        if len(found_users) > 0:
            return found_users[0]
        return None

    @staticmethod
    def update_user(user: User):
        index = users.index(user)
        if index >= 0:
            users[index] = user

    @staticmethod
    def delete_user(user: User):
        index = users.index(user)
        if index >= 0:
            users.remove(user)

    # author
    @staticmethod
    def create_author(author: Author):
        authors.append(author)

    @staticmethod
    def read_author(firstname: str, lastname: str) -> Optional[Author]:
        found_authors = [x for x in authors if x.firstname == firstname and x.lastname == lastname]
        if len(found_authors) > 0:
            return found_authors[0]
        return None

    @staticmethod
    def update_author(author: Author):
        index = authors.index(author)
        if index >= 0:
            authors[index] = author

    @staticmethod
    def delete_author(author: Author):
        index = authors.index(author)
        if index >= 0:
            authors.remove(author)

    # publisher
    @staticmethod
    def create_publisher(publisher: Publisher):
        publishers.append(publisher)

    @staticmethod
    def read_publisher(name: str) -> Optional[Publisher]:
        found_publishers = [x for x in publishers if x.name == name]
        if len(found_publishers) > 0:
            return found_publishers[0]
        return None

    @staticmethod
    def update_publisher(publisher: Publisher):
        index = publishers.index(publisher)
        if index >= 0:
            publishers[index] = publisher

    @staticmethod
    def delete_publisher(publisher: Publisher):
        index = publishers.index(publisher)
        if index >= 0:
            publishers.remove(publisher)

    # invoice
    @staticmethod
    def create_invoice(invoice: Invoice):
        invoices.append(invoice)

    @staticmethod
    def read_invoice(id: str) -> Optional[Invoice]:
        found_invoices = [x for x in invoices if x.id == id]
        if len(found_invoices) > 0:
            return found_invoices[0]
        return None

    @staticmethod
    def update_invoice(invoice: Invoice):
        index = invoices.index(invoice)
        if index >= 0:
            invoices[index] = invoice

    @staticmethod
    def delete_invoice(invoice: Invoice):
        index = invoices.index(invoice)
        if index >= 0:
            invoices.remove(invoice)
