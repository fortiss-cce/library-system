from datetime import datetime
import uuid

from library.model.user import User
from library.model.book import BorrowedBook, Book
from library.payment.credit_card import CreditCard
from library.payment.paypal import PAYPAL_ACCOUNT_BALANCE, PAYPAL_DATA_BASE
from library.persistence.storage import LibraryRepository


class Invoice:

    id: str
    books: list[BorrowedBook]
    customer: User
    is_closed: bool = False

    def __init__(self, user: User):
        self.id = str(uuid.uuid4())
        self.customer = user
        self.books = []

    def add_book(self, book: BorrowedBook):
        self.books.append(book)

    def __str__(self):
        invoice_books = "\n".join(str(book) + ": " + str(book.current_fee) for book in self.books)
        return f"""-- Invoice (id: {self.id}) --
            This is the invoice for customer '{self.customer.firstname} {self.customer.lastname}' ({self.customer.email})
            Returned books: {len(self.books)}

            {invoice_books}

            -----------------------------------------
            
            Total amount after discount: {self.calculate_fee(self.customer)[0]} €
            Gained reading credits for your next purchase: {self.calculate_fee(self.customer)[1]}
            The invoice is {'' if self.is_closed else 'not'} paid."""

    def calculate_fee(self, user: User) -> tuple[float, int]:
        price_per_book: float = 3.55
        min_books_for_discount: int = 3
        discount_per_book: float = 0.5
        discount_per_reading_credit: float = 0.5
        current_reading_credits = user.reading_credits
        reading_credits: int = user.get_reading_credits(
            [Book.from_borrowed_book(book) for book in self.books]
        )
        price: float = len(self.books) * price_per_book
        for book in self.books:
            price += book.current_fee
        discount_count: int = max(0, len(self.books) - min_books_for_discount)
        discount: float = discount_count * discount_per_book
        discount += current_reading_credits * discount_per_reading_credit
        return (
            round(price - discount if price - discount > 0.0 else 0.0, 2),
            reading_credits,
        )

    def process_invoice_with_credit_card_detail(
        self, number: str, cvv: str, expiration: datetime
    ) -> bool:
        card = CreditCard(number, expiration, cvv)
        return self.process_invoice_with_credit_card(card)

    def process_invoice_with_credit_card(self, card: CreditCard) -> bool:
        if self.is_closed:
            # payment is already processed
            return True
        # validate card information
        if not self._card_is_present_and_valid(card):
            raise ValueError("Payment information is not set or not valid")
        fee, reading_credits = self.calculate_fee(self.customer)
        is_paid: bool = self._pay_with_credit_card(card, fee)
        if is_paid:
            self.is_closed = True
            LibraryRepository.update_invoice(self)
            self.customer.reading_credits = reading_credits
            LibraryRepository.update_user(self.customer)

        return is_paid

    def _card_is_present_and_valid(self, card: CreditCard) -> bool:
        return card is not None and card.check_validity()

    def process_invoice_with_paypal(self, email: str, password: str) -> bool:
        if self.is_closed:
            # payment is already processed
            return True
        # validate account information
        if (
            email is None
            or password is None
            or password != PAYPAL_DATA_BASE.get(email, None)
        ):
            raise ValueError("Payment information is not set or not valid")
        fee, reading_credits = self.calculate_fee(self.customer)
        is_paid: bool = self._pay_with_paypal(email, password, fee)
        if is_paid:
            self.is_closed = True
            LibraryRepository.update_invoice(self)
            self.customer.reading_credits = reading_credits
            LibraryRepository.update_user(self.customer)

        return is_paid

    def _pay_with_paypal(self, email: str, password: str, fee: float) -> bool:
        if (
            email is None
            or password is None
            or password != PAYPAL_DATA_BASE.get(email, None)
        ):
            return False
        if PAYPAL_ACCOUNT_BALANCE[email] >= fee:
            PAYPAL_ACCOUNT_BALANCE[email] = PAYPAL_ACCOUNT_BALANCE[email] - fee
            print(f"Paying {fee} using PayPal")
        return True

    def _pay_with_credit_card(self, card: CreditCard, fee: float) -> bool:
        if not self._card_is_present_and_valid(card):
            return False
        remaining_amount: float = card.amount - fee
        if remaining_amount < 0:
            print(f"Card limit reached - Balance: {remaining_amount}")
            return False
        card.amount = remaining_amount
        return True
