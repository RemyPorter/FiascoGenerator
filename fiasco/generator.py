from . import model

class Connection(object):
    def __init__(self, left, right, relationship, detail):
        self.left = left
        self.right = right
        self.relationship = relationship
        self.detail = detail

class ConnectionModel(object):
    """The build method should yield a tuple of every
    possible character combination for this connection model."""
    def __init__(self, character_set):
        self.character_set = character_set

    def build(self):
        """Should yield a tuple of characters."""
        pass

class Circular(ConnectionModel):
    """A circular connection model, that is to say,
    the basic loop around the table that is a standard
    Fiasco

    >>> c = Circular(["Joebob", "Sallybob", "Jimbob"])
    >>> l = []
    >>> for tpl in c.build():
    ...   l.append(tpl)
    >>> l
    [('Jimbob', 'Joebob'), ('Joebob', 'Sallybob'), ('Sallybob', 'Jimbob')]
    """
    def __init__(self, character_set):
        ConnectionModel.__init__(self, character_set)

    def build(self):
        prev = self.character_set[-1]
        for c in self.character_set:
            yield prev, c
            prev = c

if __name__ == '__main__':
    import doctest
    doctest.testmod()
