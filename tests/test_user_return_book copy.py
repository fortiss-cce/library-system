from typing import Optional
from pytest_bdd import scenario, given, when, then
from library.model.book import Book, BorrowedBook

from library.model.user import User
from library.payment.invoice import Invoice
from library.persistence.storage import LibraryRepository
from tests.utils import create_test_book, create_test_user


@scenario("return_book.feature", "Returning a book that is borrowed by the user")
def test_return_avaiable():
    pass


@scenario("return_book.feature", "Returning a book that is not borrowed by the user")
def test_return_unavailable():
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
    return borrowed


@given("I did not borrow the book", target_fixture="borrowed")
def book_not_borrowed():
    return None


@when("I return the book", target_fixture="invoice")
def return_book(user: User, borrowed: BorrowedBook):
    invoice: Optional[Invoice] = user.return_books([borrowed])
    return invoice


@then("I should receive an invoice")
def receive_invoice(invoice: Invoice):
    assert invoice is not None


@then("the invoice should be valid")
def invoice_correct(invoice: Invoice, borrowed: BorrowedBook):
    assert len(invoice.books) == 1
    assert invoice.books[0] == borrowed


@then("an invoice should be created in the storage")
def invoice_exists(invoice: Invoice):
    assert LibraryRepository.read_invoice(invoice.id) is not None


@then("the book availability should be updated")
def availability_updated(borrowed: BorrowedBook, book: Book):
    assert borrowed.existing_items - borrowed.borrowed_items == 1
    updated_book = LibraryRepository.read_book(book.isbn)
    assert updated_book is not None
    assert updated_book.borrowed_items == 0
    assert updated_book.existing_items == 1


@then("I should not receive an invoice")
def error_message(invoice: Invoice):
    assert invoice is None


@then("the book availability should not change")
def availability_not_updated(borrowed: BorrowedBook, book: Book):
    assert borrowed is None
    updated_book = LibraryRepository.read_book(book.isbn)
    assert updated_book is not None and updated_book.borrowed_items == 0
    assert updated_book is not None and updated_book.existing_items == 1
