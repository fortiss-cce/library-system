class Author:

    fullname: str

    def __init__(self, fullname: str):
        self.fullname = fullname

        def get_firstname(self) -> str:
            name_parts = self._split_name_parts()
            return name_parts[0]

    def get_lastname(self) -> str:
        name_parts = self._split_name_parts()
        return name_parts[-1]

    def _split_name_parts(self) -> list[str]:
        return self.fullname.split()

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Author):
            return self.fullname == other.fullname
        return NotImplemented
