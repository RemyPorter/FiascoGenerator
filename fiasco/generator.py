from . import model

class Connection(object):
    def __init__(self, left, right, relationship, detail):
        self.left = left
        self.right = right
        self.relationship = relationship
        self.detail = detail

class ConnectionModel(object):
    """The build method should yield a tuple of every
    possible character combination for this connection model.

    These should be one-off generators that stop iterating."""
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

class SimpleChoiceModel(object):
    """How to choose what *kinds* of details. This should be
    an infinite iterator that returns sections with a chosen behavior.

    >>> mock = model.Playset("foo")
    >>> s = mock.new_section("Test1")
    >>> s = mock.new_section("Test2")
    >>> count = 0
    >>> stop = 4
    >>> res = []
    >>> model = SimpleChoiceModel(mock)
    >>> for s in model.choices():
    ...   res.append(s)
    ...   count += 1
    ...   if (count > stop):
    ...     break
    >>> res
    ['Test1', 'Test2', 'Test1', 'Test2', 'Test1']
    """
    def __init__(self, playset):
        self.sections = []
        for (k,v) in playset.sections.items():
            if (k.lower() == "relationships"):
                continue
            self.sections.append(k)

    def choices(self):
        idx = 0
        while (True):
            yield self.sections[idx]
            idx = (idx + 1) % len(self.sections)




if __name__ == '__main__':
    import doctest
    doctest.testmod()
