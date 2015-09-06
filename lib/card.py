from math import floor

class Card():
    def __init__(self, name, order):
        self.name = name
        self.order = order

    def __lt__(self, other):
        return self.order < other.order

    def __eq__(self, other):
        return self.name.lower() == other.name.lower()

    def __hash__(self):
        h = int(floor(self.order * 10))
        c = 1
        for i in self.name.lower():
            h += ord(i) ** c
            h %= 104729
        return h

    def __str__(self):
        ones = int(floor(self.order))
        decimals = int(floor(self.order * 10)) - ones * 10
        
        
        return "%d.%d\t%s" % (ones, decimals, self.name.title())
