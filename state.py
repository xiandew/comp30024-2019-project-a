class State(dict):
    """
    State class inherits from built-in dict. Make it immutable, hashable and
    comparable for compatible with the referenced search algorithms from AIMA.

    It is used to store a state of the board which is defined by all cells on
    the board and their corresponding states (whether the cell is empty,
    blocked or occupied by a piece).

    Acknowledgement: This code is referenced from official python developer's
    guide <https://www.python.org/dev/peps/pep-0351/#sample-implementations>
    """

    def _immutable(self, *args, **kws):
        raise TypeError('State is immutable')

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    update = _immutable
    setdefault = _immutable
    pop = _immutable
    popitem = _immutable

    def __hash__(self):
        return hash(str(self))

    def __lt__(self, other):
        return str(self) < str(other)
