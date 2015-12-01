from core import Draw
from core import Pretty

_len_tab = None  # set in generator
_iroot = None  # set in generator


def generator(root, target=None ):
    """
    Create a generator to enumerate Levels from root of the Grid.
    Argument target limits traversal, can be int() or iterable, see also Level.next_level.
    """
    global _len_tab, _iroot

    m = len(root)
    root = Draw(root)

    if target is not None:
        if not hasattr(target, '__len__'):
            roof = int(target)
            target = Draw([0] * m)
        elif len(target) == m:
            roof = sum( root ) - sum(target)
            target = Draw(target)
            if not Draw([0] * m) <= target <= root:
                raise ValueError( "argument should be between %s and %s" % ([0] * m, list(root)) )
        else:
            raise ValueError( "argument has different number of categories (%d) than Grid.roof (%d)" %
                              (len(target), m) )
    else:
        target = Draw([0] * m)
        roof = sum(root)

    _iroot = [ sum(root[:i]) - sum(target[:i]) for i in range(m) ]
    _len_tab = [ [1] for _ in range(m) ]

    previous = [ root ]
    yield previous
    for n in range( roof ):
        current = next_level( previous, root, roof, n, target )
        yield current
        previous = current

def _read_len_tab( n, i ):
    global _len_tab, _iroot
    # unsafe, since _len_tab is filled during generation
    n_ast = n - _iroot[i]
    return _len_tab[i][n_ast] if n_ast >= 0 else 0

def P(level):
    return (d.P for d in level)


#zigzag
def next_level( level, root, roof, n=None, target=None ):

    """
    Enumerate the next Level.
    From each Draw draw one farther element and calculates the probabilities of them.
    The argument target limits the enumeration to only those events from which the target is reachable.
    The argument n can be given which equals to the number of the Levels already enumerated.
    """

    m = len(root)
    denominator = roof - n

    flush = [ None ] * m
    drawptr = [ _read_len_tab( n, i ) for i in range( 1, m ) ]
    drawptr.append( 0 )

    following = Pretty()

    for i, d in enumerate( level ):
        num_of_0s = d.gamma - sum( x > target[j] for j, x in enumerate(d[:d.gamma]) )
        for k in range( d.gamma, m ):
            flush[ k - num_of_0s ] = len( following )

            # enumerating descendants
            if d[k] > target[k]:
                p = d.P * d[k]
                drawptr[k] += 1

                # finding other ascendants
                for j, c in enumerate( d ):
                    if j != k and c < root[j]:
                        # skipping
                        if drawptr[j] <= i:
                            drawptr[j] = i + ( _read_len_tab( n - sum(target) + sum(d[:j]), j + 1 ) or 1 )
                        # stepping
                        p += level[drawptr[j]].P * (c + 1)
                        drawptr[j] += 1

                child = Draw( d, k, p / denominator )
                child[k] -= 1
                following.append( child )

            else:
                num_of_0s += 1

    # storing length of shifted level of each fixed prefix sublattice
    for i, f in enumerate( flush ):
        if f is not None:
            _len_tab[i].append( len( following ) - f )

    return following


