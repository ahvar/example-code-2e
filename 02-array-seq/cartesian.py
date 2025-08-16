"""
"""
import pprint
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)
class Cartesian:
    def __init__(self, colors=None, sizes=None):
        self._colors = colors
        self._sizes = sizes

    def tshirts_from_listcomp(self, colors, sizes):
        return [(color, size) for color in colors for size in sizes]
    
    def tshirt_from_genexp(self, colors, sizes):
        for shirt in (f'{color} {size}' for color in colors for size in sizes):
            print(shirt)

    def __iter__(self):
        """
        The returned generator is an iterator, so client code looping through
        it calls __next__() to get each (color, size); until it raises
        StopIteration
        """
        return ((color, size) for color in self._colors for size in self._sizes)
    
class OtherCartesian:
    def __init__(self, colors, sizes):
        self._colors = colors
        self._sizes = sizes

    def __iter__(self):
        for color in self._colors:
            for size in self._sizes:
                yield (color, size)



if __name__ == "__main__":
    #cartesian = Cartesian()
    colors = ['black','white']
    sizes = ['S','M','L']
    #tshirts = cartesian.tshirt_from_genexp(colors, sizes)
    #pp.pprint(tshirts)
    for tshirt in Cartesian(colors, sizes):
        print(tshirt)
    
