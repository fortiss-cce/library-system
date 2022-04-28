from copy import copy
from datetime import timedelta
from pytest_bdd import scenario, given, when, then
from library.model.book import Book, BorrowedBook

from library.model.user import User
from library.persistence.storage import LibraryRepository
from tests.utils import create_test_book, create_test_user


@scenario("renew_rental_book.feature", "Renewing the rental")
def test_renew_rental():
    pass


@given("I'm an user", target_fixture="user")
def user():
    return create_test_user()


@given("I know a book", target_fixture="book")
def book():
    return create_test_book()


@given("I have borrowed that book", target_fixture="borrowed")
def book_borrowed(user: User, book: Book):
    borrowed = user.borrow_book(book)
    return copy(borrowed)


@when("I renew the book rental", target_fixture="renewed")
def renew_rental(user: User):
    assert len(user.borrowed_books) == 1
    renewed = user.borrowed_books[0].renew_rental()
    return renewed


@then("I should have the book borrowed")
def correct_borrowed_book(user: User, renewed: BorrowedBook):
    assert len(user.borrowed_books) == 1
    assert user.borrowed_books[0] == renewed


@then("I should not get an invoice")
def no_invoice(user: User):
    assert len(user.invoices) == 0


@then("the book should not be marked as read")
def no_read_books(user: User):
    assert len(user.read_books) == 0


@then("the rental time should be increased")
def time_increased(borrowed: BorrowedBook, renewed: BorrowedBook):
    assert borrowed is not None
    assert renewed is not None
    assert borrowed.due_date < renewed.due_date
    assert borrowed.due_date + timedelta(days=7) == renewed.due_date


@then("the current fee should be increased")
def fee_increased(borrowed: BorrowedBook, renewed: BorrowedBook):
    assert borrowed is not None
    assert renewed is not None
    assert borrowed.current_fee < renewed.current_fee


@then("the book availability should not change")
def availability_not_updated(borrowed: BorrowedBook, renewed: BorrowedBook, book: Book):
    assert book.isbn == borrowed.isbn and book.isbn == renewed.isbn
    updated_book = LibraryRepository.read_book(renewed.isbn)
    assert updated_book is not None and updated_book.borrowed_items == 1
    assert updated_book is not None and updated_book.existing_items == 1


@then("the user should have the correct borrowed book")
def user_updated(user: User, renewed: BorrowedBook):
    updated_user = LibraryRepository.read_user(user.email)
    assert updated_user is not None
    assert len(updated_user.borrowed_books) == 1
    updated_book = updated_user.borrowed_books[0]
    assert updated_book is not None
    assert updated_book == renewed
    assert updated_book.current_fee == renewed.current_fee
    assert updated_book.due_date == renewed.due_date
