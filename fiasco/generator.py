from . import model
import itertools
import collections
import random

class Connection(object):
    def __init__(self, left, right, relationship, detail):
        self.left = left
        self.right = right
        self.relationship = relationship
        self.detail = detail

    def __repr__(self):
        return """
        ----------------
        {0} / {1}
        Relationship: {2}
        Detail: {3}
        ----------------""".format(self.left, self.right,
            self.relationship, self.detail)

class ConnectionStrategy(object):
    """The build method should yield a tuple of every
    possible character combination for this connection model.

    These should be one-off generators that stop iterating."""
    def __init__(self, character_set):
        self.character_set = character_set

    def build(self):
        """Should yield a tuple of characters."""
        pass

class Circular(ConnectionStrategy):
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
        ConnectionStrategy.__init__(self, character_set)

    def build(self):
        prev = self.character_set[-1]
        for c in self.character_set:
            yield prev, c
            prev = c

class CombinationPairings(ConnectionStrategy):
    """A connection model that takes your population and
    finds every possible combination

    >>> cp = CombinationPairings(["Joebob", "Jimbob", "Sallybob"])
    >>> res = []
    >>> for tpl in cp.build():
    ...   res.append(tpl)
    >>> res
    [('Joebob', 'Jimbob'), ('Joebob', 'Sallybob'), ('Jimbob', 'Sallybob')]
    """

    def __init__(self, character_set):
        ConnectionStrategy.__init__(self, character_set)

    def build(self):
        for a,b in itertools.combinations(self.character_set, 2):
            yield a,b

class RandomPairings(ConnectionStrategy):
    """A connection model that builds random pairings, without
    repeats. Every name will appear *at least* twice.

    >>> import functools
    >>> rp = RandomPairings(["Joebob", "Jimbob", "Sallybob"])
    >>> l = []
    >>> for tpl in rp.build():
    ...   l.append(tpl)
    >>> len(l) >= 3
    True
    """

    def __init__(self, character_set):
        ConnectionStrategy.__init__(self, character_set)
        self.names = {name:list() for name in character_set}
        self.consumed = set()
        self.namecount = collections.defaultdict(int)

    def done(self):
        """
        Is the process done (has at least two connections for each character?)

        >>> rp = RandomPairings(["Joebob", "Jimbob", "Sallybob"])
        >>> rp.namecount["Joebob"] = 2
        >>> rp.done()
        False
        >>> rp.namecount["Jimbob"] = 3
        >>> rp.namecount["Sallybob"] = 2
        >>> rp.done()
        True
        """
        return len(list(itertools.ifilter(lambda x: x >= 2,
            self.namecount.values()))) == len(self.character_set)

    def build(self):
        for a,b in itertools.combinations(self.character_set, 2):
            self.names[a].append((a,b))
            self.names[b].append((a,b))
        while not self.done():
            n = random.choice(self.character_set)
            possible = random.choice(self.names[n])
            if possible in self.consumed:
                continue
            yield possible
            self.consumed.add(possible)
            a,b = possible
            self.namecount[a] += 1
            self.namecount[b] += 1






class SimpleSectionChoiceStrategy(object):
    """How to choose what *kinds* of details. This should be
    an infinite iterator that returns sections with a chosen behavior.

    >>> count = 0
    >>> stop = 4
    >>> res = []
    >>> model = SimpleSectionChoiceStrategy(mock)
    >>> for s in model.choices():
    ...   res.append(s)
    ...   count += 1
    ...   if (count > stop):
    ...     break
    >>> res
    ['test1', 'test2', 'test1', 'test2', 'test1']
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

class Setup(object):
    """
    The setup for a Fiasco, controlled by Connection and Choice models.

    >>> s = Setup(mock, ["Joebob", "Jimbob", "Sallybob"], Circular, SimpleSectionChoiceStrategy)
    >>> f = s.build()
    >>> len(f)
    3
    >>> f[0].left
    'Sallybob'
    >>> f[0].right
    'Joebob'
    >>> f[1].left
    'Joebob'
    >>> f[1].right
    'Jimbob'
    """
    def __init__(self, playset, characters, ConnectionStrategyType=Circular, SectionChoiceStrategyType=SimpleSectionChoiceStrategy):
        self.playset = playset
        self.characters = characters
        self.connections = ConnectionStrategyType(characters)
        self.choices = SectionChoiceStrategyType(playset).choices()
        self.fiasco = []

    def build(self):
        fiasco = []
        for (a,b) in self.connections.build():
            section_name = next(self.choices)
            fiasco.append(
                Connection(a, b, self.playset["relationships"].random_item(),
                self.playset[section_name].random_item()))
        return fiasco



if __name__ == '__main__':
    import doctest
    mock = model.Playset("foo")
    s = mock.new_section("Relationships").new_category("family").add_item("Parent / Child").add_item("Cousins")
    s = mock["relationships"].new_category("work").add_item("Co-workers").add_item("boss / employee")
    s = mock.new_section("Test1").new_category("foo").add_item("ABC").add_item("DEF")
    s = mock.new_section("Test2").new_category("bar").add_item("BCD").add_item("EFG")
    doctest.testmod()
