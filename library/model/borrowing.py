from library.model.book import Book
from library.model.user import User
from datetime import datetime, timedelta
from library.persistence.storage import LibraryRepository


class Borrowing:
    book: Book
    user: User
    due_date: datetime
    fee: float

    def __init__(self, book:Book, user:User, due_date: datetime):
        self.book = book
        self.user = user
        self.fee = book.get_weekly_fee()
        self.due_date = due_date

    def open_borrowing(self):
        try:
            if self.book.can_borrow():
                if self.book._book_type == "Paper":
                    self.book.borrowed_items += 1
                self._update_library_repository()
            return
        except AttributeError:
            raise AttributeError("Attribute error")
        except ValueError:
            raise ValueError("Book cannot be borrowed")

    def renew_borrowing(self):
        self.due_date += timedelta(days=7)
        self.fee += self.book.get_weekly_fee()

    def close_borrowing(self):
        if self.book._book_type == "Paper":
            self.book.borrowed_items -= 1
        self._update_library_repository()

    def add_fee_to_user_account(self):
        pass

    def _update_library_repository(self):
        LibraryRepository.update_book(self.book)
        LibraryRepository.update_user(self.user)

    def get_book(self):
        return self.book

    def get_user(self):
        return self.user



