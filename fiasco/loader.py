"""Parse a Fiasco Playset into a set of relationship types.

>>> from StringIO import StringIO
>>> f = StringIO()
>>> f.writelines(["Test\\n", "# RELATIONSHIPS\\n", "## 1 Family\\n", "1 Parent / Child\\n", "2 Cousins\\n"])
>>> f.seek(0)
>>> print f.getvalue()
Test
# RELATIONSHIPS
## 1 Family
1 Parent / Child
2 Cousins
<BLANKLINE>
>>> playset = process(f)
>>> playset.name
'Test'
>>> playset["relationships"]["family"].items
['Parent / Child', 'Cousins']
"""

from . import model

SECTION_HEADER = "#"
CAT_HEADER = SECTION_HEADER * 2

def parse_line(line):
    """Break the input line into a tuple
    >>> parse_line("5 this is a test")
    (5, 'this is a test')
    """
    first_space = line.index(" ")
    return (int(line[0:first_space].strip()), line[first_space:].strip())

def skip(line, header):
    return line[len(header):].strip()

def build_playset(line):
    return model.Playset(line.strip())

def build_section(playset, line):
    title = skip(line, SECTION_HEADER)
    return playset.new_section(title.lower())

def build_cat(section, line):
    title = parse_line(skip(line, CAT_HEADER))[1]
    return section.new_category(title.lower())

def is_cat(line):
    """
    >>> is_cat("## Foo")
    True
    >>> is_cat("# Foo")
    False
    >>> is_cat("Nope")
    False
    """
    return line.startswith(CAT_HEADER)

def is_section(line):
    """
    >>> is_section("# Foo")
    True
    >>> is_section("## Foo")
    False
    >>> is_section("Nope.")
    False
    """
    return line.startswith(SECTION_HEADER) and not is_cat(line)

def process(filehandle):
    current_section = None
    current_cat = None
    first_line = True
    playset = None
    linecount = 0
    first_section = True
    first_cat = True
    for line in filehandle:
        linecount += 1
        if first_line:
            playset = build_playset(line)
            first_line = False
        elif is_section(line):
            assert(linecount == 2 or not first_section) #second line must be a section
            current_section = build_section(playset, line)
            first_section = False
        elif is_cat(line):
            assert(linecount == 3 or not first_cat) #third line must be a category
            current_cat = build_cat(current_section, line)
            first_cat = False
        else:
            current_cat.add_item(parse_line(line)[1])
    return playset

if __name__ == '__main__':
    import doctest
    doctest.testmod()