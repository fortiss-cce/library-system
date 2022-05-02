from datetime import datetime, timedelta

from library.model.author import Author
from library.model.genre import Genre
from library.model.publisher import Publisher
from library.model.book import Book
from library.model.user import User
from library.payment.credit_card import CreditCard
from library.persistence.storage import LibraryRepository


def create_test_book(available=True):
    a1 = Author("Eric","Topol")
    LibraryRepository.create_author(a1)
    p1 = Publisher("Basic Books")
    LibraryRepository.create_publisher(p1)
    b1 = Book(
        "Deep Medicine: How Artificial Intelligence Can Make Healthcare Human Again",
        [a1],
        p1,
        datetime(2019, 3, 12),
        [Genre.MEDICINE, Genre.COMPUTER_SCIENCE],
        400,
        "1541644638",
        "Paper",
        0,
        1,
        0 if available else 1,
    )
    LibraryRepository.create_book(b1)
    return b1


def create_test_user():
    u1 = User(
        "max@test.org",
        "Max",
        "Mustermann",
        "78234892",
        "2374823442342",
        "89",
        "3284923495",
        "49",
    )
    LibraryRepository.create_user(u1)
    return u1


def create_test_credit_card_info(valid=True):
    if valid:
        return CreditCard("247912434", datetime.now() + timedelta(days=100), "111")
    return CreditCard("", datetime.now(), "000")


def create_test_paypal_info(valid=True):
    if valid:
        return "amanda1985", "PaSsW0rD"
    return "Hugo", "123"
