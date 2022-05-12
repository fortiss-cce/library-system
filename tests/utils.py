from datetime import datetime, timedelta

from library.model.author import Author
from library.model.genre import Genre
from library.model.publisher import Publisher
from library.model.book import PaperBook
from library.model.user import User
from library.payment.credit_card import CreditCard
from library.persistence.storage import LibraryRepository


def create_test_book(available=True):
    a1 = Author("Eric", "Topol")
    LibraryRepository.create_author(a1)
    p1 = Publisher("Basic Books")
    LibraryRepository.create_publisher(p1)
    b1 = PaperBook(
        title="Deep Medicine: How Artificial Intelligence Can Make Healthcare Human Again",
        authors=[a1],
        publisher=p1,
        pub_date=datetime(2019, 3, 12),
        genres=[Genre.MEDICINE, Genre.COMPUTER_SCIENCE],
        pages=400,
        isbn="1541644638",
        borrowed_items=0,
        existing_items=1,
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
