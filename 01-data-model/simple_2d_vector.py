"""
Vector class implementing the:
 '+' operator
 abs() to return the absolute value of integers and floats, and the magnitude of complex numbers
 '*' operator to perform scalar multiplication (i.e. make a new vector with the same direction and a multiplied magnitude)


Note the implementation of five special methods and that none are called directly within the class and would not be called
in usage of the class by client code. The interpreter is the only frequent caller of most special methods / dunder methods
"""

import math

class Vector:
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    def __repr__(self):
        # !r is a conversion specifier, calling __repr__() on self._x
        return f'Vector({self._x!r}, {self._y!r})'
    
    def __abs__(self):
        return math.hypot(self._x,self._y)
    
    def __bool__(self):
        """
        abs(self) calls self.__abs__() which returns the magnitude
        bool() converts that magnitude to a boolean value
        """
        return bool(abs(self))
    
    def __add__(self, other):
        x = self._x + other.x
        y = self._y + other.y
        return Vector(x, y)
    
    def __mul__(self, scalar):
        """
        NOTE: as is, this violates the commutative property of
        scalar multiplication
        """
        return Vector(self._x * scalar, self._y * scalar)

    