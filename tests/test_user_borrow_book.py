from pytest_bdd import scenario, given, when, then
from library.model.book import Book, BorrowedBook

from library.model.user import User
from library.persistence.storage import LibraryRepository
from tests.utils import create_test_book, create_test_user


@scenario("borrow_book.feature", "Borrowing a book that is available")
def test_borrow_avaiable():
    pass


@scenario("borrow_book.feature", "Borrowing a book that is unavailable")
def test_borrow_unavailable():
    pass


@given("I'm an user", target_fixture="user")
def user():
    return create_test_user()


@given("I want to to borrow an available book", target_fixture="book")
def book_available():
    return create_test_book(available=True)


@given("I want to to borrow an unavailable book", target_fixture="book")
def book_unavailable():
    return create_test_book(available=False)


@when("I borrow the book", target_fixture="borrowed")
def borrow_book(user: User, book: Book):
    return user.borrow_book(book)


@then("I should receive a borrowed book")
def no_error_message(borrowed: BorrowedBook):
    assert borrowed is not None


@then("I should not receive/borrow book")
def error_message(borrowed: BorrowedBook):
    assert borrowed is None


@then("the book availability should be updated")
def availability_updated(borrowed: BorrowedBook, book: Book):
    assert borrowed.existing_items - borrowed.borrowed_items == 0
    updated_book = LibraryRepository.read_book(book.isbn)
    assert updated_book is not None and updated_book.borrowed_items == 1


@then("the book availability should not change")
def availability_not_updated(borrowed: BorrowedBook, book: Book):
    assert borrowed is None
    updated_book = LibraryRepository.read_book(book.isbn)
    assert updated_book is not None and updated_book.borrowed_items == 1
