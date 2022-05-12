from dataclasses import dataclass


@dataclass
class BookPrice:
    price_per_book: float = 3.55
    min_books_for_discount: int = 3
    discount_per_book: float = 0.5
    discount_per_reading_credit: float = 0.5
