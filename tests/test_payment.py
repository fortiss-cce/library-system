from typing import Optional
import pytest
from pytest_bdd import scenario, given, when, then
from library.model.book import Book, BookBorrowed

from library.model.user import User
from library.payment.credit_card import CreditCard
from library.payment.invoice import Invoice
from library.persistence.storage import LibraryRepository
from tests.utils import (
    create_test_book,
    create_test_user,
    create_test_credit_card_info,
    create_test_paypal_info,
)
from library.payment.paypal import PAYPAL_ACCOUNT_BALANCE


@pytest.fixture(scope="function")
def context():
    return {"exception": None}


@scenario("payment.feature", "Receiving an invoice the invoice should be valid")
def test_return_avaiable():
    pass


@scenario(
    "payment.feature",
    "Paying an invoice with credit card should fail if the card is not valid",
)
def test_pay_credit_card_fail_card_info():
    pass


@scenario(
    "payment.feature",
    "Paying an invoice with credit card should fail if the cards limit is smaller then the amount to pay",
)
def test_pay_credit_card_fail_amount():
    pass


@scenario(
    "payment.feature",
    "Paying an invoice with credit card should succeed if all info is correct",
)
def test_pay_credit_card_success():
    pass


@scenario(
    "payment.feature",
    "Paying an invoice with PayPal should fail if the account information is false",
)
def test_pay_paypal_fail_account():
    pass


@scenario(
    "payment.feature",
    "Paying an invoice with PayPal should succeed if all info is correct",
)
def test_pay_paypal_success():
    pass


@given("there is a user", target_fixture="user")
def user():
    return create_test_user()


@given("the user has borrowed a book", target_fixture="borrowed")
def book_borrowed(user: User):
    book: Book = create_test_book()
    borrowed = user.borrow_book(book)
    return borrowed


@given("the user returns the book", target_fixture="invoice")
def return_book(user: User, borrowed: BookBorrowed):
    invoice: Optional[Invoice] = user.return_books([borrowed])
    return invoice


@given("the invoice exists")
def invoice_exists(invoice: Invoice):
    assert invoice is not None
    assert LibraryRepository.read_invoice(invoice.id) is not None


@when("I check the invoice")
def check_invoice():
    pass


@then("the customer should be correct")
def invoice_customer_correct(invoice: Invoice, user: User):
    assert invoice.customer == user


@then("the items on the invoice should be correct")
def invoice_items_correct(invoice: Invoice, borrowed: BookBorrowed):
    assert len(invoice.books) == 1
    assert invoice.books[0] == borrowed


@then("the invoice should not be closed")
def invoice_not_closed(invoice: Invoice):
    assert not invoice.is_closed


@then("the invoice should be closed")
def invoice_closed(invoice: Invoice):
    assert invoice.is_closed


@when("the user has a non valid credit card", target_fixture="card")
def credit_card_not_valid():
    return create_test_credit_card_info(valid=False)


@when("the user has a valid credit card", target_fixture="card")
def credit_card_valid():
    return create_test_credit_card_info(valid=True)


@when("the user has a non valid PayPal account", target_fixture="paypal")
def paypal_not_valid():
    return create_test_paypal_info(valid=False)


@when("the user has a valid PayPal account", target_fixture="paypal")
def paypal_valid():
    return create_test_paypal_info(valid=True)


@when("the user pays with this card")
def user_pays_card(context, invoice: Invoice, card: CreditCard):
    try:
        invoice.process_invoice_with_credit_card(card)
    except ValueError as e:
        context["exception"] = e


@when("the user pays with PayPal")
def user_pays_paypal(context, invoice: Invoice, paypal: tuple[str, str]):
    try:
        invoice.process_invoice_with_paypal(paypal[0], paypal[1])
    except ValueError as e:
        context["exception"] = e


@then("an exception should be raised")
def payment_exception(context):
    assert context["exception"] is not None


@when("the limit of the card is lower than the fee")
def credit_card_low_limit(card: CreditCard):
    card.amount = 0


@when("the limit of the card is higher than the fee")
def credit_card_high_limit(user: User, card: CreditCard, invoice: Invoice):
    user.reading_credits = 0
    card.amount = invoice.calculate_fee(user) + 1.0


@then("the card limit should not change")
def credit_card_unchanged(card: CreditCard):
    assert card.amount == 0


@then("the card limit should be updated")
def credit_card_changed(card: CreditCard):
    assert card.amount == 1.0


@then("the account balance should be updated")
def account_balance_changed(paypal, invoice: Invoice, user: User):
    user.reading_credits = 0
    assert PAYPAL_ACCOUNT_BALANCE[paypal[0]] == 100.0 - invoice.calculate_fee(user)


@then("the invoice should be updated in storage")
def credit_card_updated(invoice: Invoice):
    updated_invoice = LibraryRepository.read_invoice(invoice.id)
    assert updated_invoice is not None and updated_invoice.is_closed
