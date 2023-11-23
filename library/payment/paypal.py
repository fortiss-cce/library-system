PAYPAL_DATA_BASE: dict[str, str] = {"amanda1985": "PaSsW0rD", "qwerty": "123456789"}
PAYPAL_ACCOUNT_BALANCE: dict[str, float] = {"amanda1985": 100.0, "qwerty": 42.0}

class Paypal:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
