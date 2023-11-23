from enum import Enum

seconds_in_a_minute = 60

class BookType(Enum):
    PAPER = "Paper"
    ELECTRONIC = "Electronic"
    AUDIO = "Audio"

class BookTypeStatic():

    @staticmethod
    def can_borrow(book):
        if (book._book_type == BookType.PAPER):
            return book.existing_items - book.borrowed_item > 0
        elif (book._book_type == BookType.ELECTRONIC):
            return True
        elif (book._book_type == BookType.AUDIO):
            return True
        else:
            raise AttributeError("No such a book...")

    @staticmethod
    def get_approximate_duration(book):
        if (book._book_type == BookType.PAPER):
            return book._pages * 3 * seconds_in_a_minute
        elif (book._book_type == BookType.ELECTRONIC):
            return book._pages * 5 * seconds_in_a_minute
        elif (book._book_type == BookType.AUDIO):
            return book._duration
        else:
            raise AttributeError("No such a book...")

    @staticmethod
    def get_weekly_fee(book):
        if (book._book_type == BookType.PAPER):
            return 5
        elif (book._book_type == BookType.ELECTRONIC):
            return 2
        elif (book._book_type == BookType.AUDIO):
            return 2
        else:
            raise AttributeError("No such a book...")

