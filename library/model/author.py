class Author:

    _firstname: str
    _lastname: str

    def __init__(self, firstname: str, lastname: str):
        self._firstname = firstname
        self._lastname = lastname
        self._uid=f"{self._firstname} {self._lastname}"

    def get_firstname(self) -> str:
        return self._firstname

    def get_lastname(self) -> str:
        return self._lastname

    def get_fullname(self) -> str:
        return self._uid

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Author):
            return self._uid == other._uid
        return NotImplemented
