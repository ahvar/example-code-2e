"""
The target of unpacking can use nesting
"""
metro_areas = [
    ('Tokyo', 'JP', 36.933, (35.689, 139.69)),
    ('Delhi NCR', 'IN', 21.935, (28.61, 77.20)),
    ('Mexico City', 'MX', 20.142, (19.43, -99.13333)),
    ('New York-Newark', 'US', 20.104, (40.8086, -74.020386))
]

def unpackit():
    print(f'{"":15} | {"latitude":>9} | {"longitude":>9}')
    for name, _, _, (lat, lon) in metro_areas:
        if lon <= 0:
            print(f'{name:15} | {lat:9.4f} | {lon:9.4f}')


def destructureit():
    print(f'{"":15} | {"latitude":>9} | {"longitude":>9}')
    for record in metro_areas:
        match record:
            case [name, _, _, (lat, lon)] if lon <= 0:
                print(f'{name:15} | {lat:9.4f} | {lon:9.4f}')

def bind_with_variable():
    """
    Unlike unpacking, patterns don't destructure iterables that are not
    sequences (such as iterators).
    You can bind any part of a pattern with a variable using the as keyword.
    """
    print(f'{"":15} | {"latitude":>9} and {"longitude":>9} ')
    for record in metro_areas:
        match record:
            case [name, _, _, (lat, lon) as coord]:
                print(f'{name:15} | {lat} and {lon}')
                print(f'{name:15} | {coord}')


if __name__ == "__main__":
    #unpackit()
    #destructureit()
    bind_with_variable()