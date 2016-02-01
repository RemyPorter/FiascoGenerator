"""
A collection of simple model objects to model a playset's tree.

>>> p = Playset("test")
>>> dummy = p.new_section("Relationships").new_category("Family").add_item("Cousins").add_item("Spouses")
>>> p["Relationships"]["Family"].items
['Cousins', 'Spouses']
"""
import random

class Category:
    def __init__(self, name):
        self.items = []
        self.name = name

    def random_item(self):
        return random.choice(self.items)

    def add_item(self, item):
        self.items.append(item)
        return self

class Section:
    def __init__(self, name):
        self.categories = dict()
        self.name = name

    def __getitem__(self, k):
        return self.categories[k]

    def random_category(self):
        return random.choice(self.categories.items())

    def new_category(self, cat_name):
        self.categories[cat_name] = Category(cat_name)
        return self.categories[cat_name]

class Playset:
    def __init__(self, name):
        self.name = name
        self.sections = dict()

    def __getitem__(self, k):
        return self.sections[k]

    def new_section(self, sect_name):
        self.sections[sect_name] = Section(sect_name)
        return self.sections[sect_name]

if __name__ == '__main__':
    import doctest
    doctest.testmod()