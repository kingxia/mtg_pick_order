from math import floor
import string

class Card():
    def __init__(self, name, order):
        self.name = name
        self.order = order

    def ratings_str(self):
        s_order = [str(o) for o in self.order]
        return '\t'.join(s_order)

    def get_name(self):
        return string.capwords(self.name)

    def __lt__(self, other):
        return self.order[0] < other.order[0]

    def __eq__(self, other):
        return self.name.lower() == other.name.lower()

    def __hash__(self):
        h = int(floor(self.order[0] * 10))
        c = 1
        for i in self.name.lower():
            h += ord(i) ** c
            h %= 104729
        return h

    def __str__(self):
        ones = int(floor(self.order[0]))
        decimals = int(floor(self.order[0] * 10)) - ones * 10

        conditional = ''
        if len(self.order) > 1:
            c_ones = int(floor(self.order[1]))
            c_decimals = int(floor(self.order[1] * 10)) - c_ones * 10
            conditional = '\t(%d.%d)' % (c_ones, c_decimals)
        
        return "%d.%d\t%s%s" % (ones, decimals, self.get_name(), conditional)
