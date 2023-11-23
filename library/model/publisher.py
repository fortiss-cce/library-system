class Publisher:
    _name: str

    def __init__(self, name):
        self._name = name

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Publisher):
            return self._name == other._name
        return NotImplemented
