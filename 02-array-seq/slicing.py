"""
The ellipsis—written with three full stops (...) and not …
(Unicode U+2026)—is recognized as a token by the Python parser.
It is an alias to the Ellipsis
As such, it can be passed as an argument to functions and as part
of a slice specification, as in f(a, ..., z) or a[i:...]. NumPy uses
... as a shortcut when slicing arrays of many dimensions; for example,
if x is a four-dimensional array, x[i, ...] is a shortcut for
x[i, :, :, :,]. See “NumPy quickstart” to learn more about this.

"""
