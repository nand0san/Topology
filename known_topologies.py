from itertools import chain, combinations
from topo import Topology


def create_discrete_topology(space):
    """
    Create a discrete topology on the given space.
    """
    # Generate all possible subsets
    subsets = list(chain.from_iterable(combinations(space, r) for r in range(len(space)+1)))
    subsets = [set(s) for s in subsets]
    return Topology(space, subsets)


def create_trivial_topology(space):
    """
    Create a trivial (indiscrete) topology on the given space.
    """
    subsets = [set(), set(space)]
    return Topology(space, subsets)


def create_sierpinski_topology():
    """
    Create the Sierpiński topology.
    """
    space = {0, 1}
    subsets = [set(), {1}, {0, 1}]
    return Topology(space, subsets)
