from datetime import datetime


class CreditCard:
    amount: float
    _number: str
    _valid_date: datetime
    _cvv: str
    _valid: bool

    def __init__(self, number: str, date: datetime, cvv: str):
        self.amount = 100000.0
        self._number = number
        self._valid_date = date
        self._cvv = cvv
        self._valid = self.check_validity()

    def is_valid(self) -> bool:
        return self._valid

    def check_validity(self) -> bool:
        # Dummy validation
        return (
            len(self._number) > 0
            and self._valid_date > datetime.now()
            and self._cvv != "000"
        )

    def pay(self, fee: float) -> bool:
        if not self._card_is_present_and_valid(self):
            return False
        remaining_amount: float = self.amount - fee
        if remaining_amount < 0:
            print(f"Card limit reached - Balance: {remaining_amount}")
            return False
        self.amount = remaining_amount
        return True
