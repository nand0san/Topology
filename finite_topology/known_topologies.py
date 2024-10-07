from itertools import chain, combinations
from .topology import Topology


def create_discrete_topology(space):
    """
    Create a discrete topology on the given space.

    A **discrete topology** on a set \(X\) is the topology in which every subset of \(X\) is open. This means the topology \(\tau\) is equal to the power set of \(X\).

    .. math::

        \tau = \mathcal{P}(X)

    Parameters:
        space (set): The set on which the topology is defined.

    Returns:
        Topology: An instance of the Topology class representing the discrete topology.
    """
    # Generate all possible subsets
    subsets = list(chain.from_iterable(combinations(space, r) for r in range(len(space) + 1)))
    subsets = [set(s) for s in subsets]
    return Topology(space, subsets)


def create_trivial_topology(space):
    """
    Create a trivial (indiscrete) topology on the given space.

    A **trivial topology** (also known as **indiscrete topology**) on a set \(X\) is the topology that only contains the empty set and the entire set itself.

    .. math::

        \tau = \{ \emptyset, X \}

    Parameters:
        space (set): The set on which the topology is defined.

    Returns:
        Topology: An instance of the Topology class representing the trivial topology.
    """
    subsets = [set(), set(space)]
    return Topology(space, subsets)


def create_sierpinski_topology():
    """
    Create the Sierpiński topology.

    The **Sierpiński topology** is defined on the set \(\{0, 1\}\) with the collection of open sets being \(\{ \emptyset, \{1\}, \{0, 1\} \}\).

    Returns:
        Topology: An instance of the Topology class representing the Sierpiński topology.
    """
    space = {0, 1}
    subsets = [set(), {1}, {0, 1}]
    return Topology(space, subsets)


def create_particular_point_topology(space, particular_point):
    """
    Create a particular point topology on the given space.

    A **particular point topology** on a set \(X\) is defined such that every non-empty open set must include a distinguished point \(p \in X\).

    Parameters:
        space (set): The set on which the topology is defined.
        particular_point: The distinguished point that must be included in all non-empty open sets.

    Returns:
        Topology: An instance of the Topology class representing the particular point topology.

    Raises:
        ValueError: If the particular point is not an element of the space.
    """
    if particular_point not in space:
        raise ValueError("The particular point must be an element of the space.")

    # All subsets that contain the particular point, plus the empty set
    subsets = [set(), set(space)]
    for r in range(1, len(space)):
        for subset in combinations(space, r):
            subset = set(subset)
            if particular_point in subset:
                subsets.append(subset)

    return Topology(space, subsets)


def create_excluded_point_topology(space, excluded_point):
    """
    Create an excluded point topology on the given space.

    An **excluded point topology** on a set \(X\) is defined such that the only open sets are those that do not contain a particular point \(e \in X\), plus the entire set and the empty set.

    Parameters:
        space (set): The set on which the topology is defined.
        excluded_point: The point that is excluded from all non-empty open sets.

    Returns:
        Topology: An instance of the Topology class representing the excluded point topology.

    Raises:
        ValueError: If the excluded point is not an element of the space.
    """
    if excluded_point not in space:
        raise ValueError("The excluded point must be an element of the space.")

    # All subsets that do not contain the excluded point, plus the entire space
    subsets = [set(), set(space)]
    for r in range(1, len(space)):
        for subset in combinations(space, r):
            subset = set(subset)
            if excluded_point not in subset:
                subsets.append(subset)

    return Topology(space, subsets)


def create_divisibility_topology(space):
    """
    Create a topology on a set of positive integers where open sets are those containing all multiples of certain elements.

    In the **divisibility topology**, an open set is defined as containing all multiples of a given element in the set.

    Parameters:
        space (set): A set of positive integers.

    Returns:
        Topology: An instance of the Topology class representing the divisibility topology.
    """
    subsets = [set(), set(space)]
    for element in space:
        multiples = {x for x in space if x % element == 0}
        subsets.append(multiples)

    # Ensure the topology is closed under arbitrary unions
    # For simplicity in finite cases, include all unions of the basic open sets
    n = len(subsets)
    for i in range(1, 2 ** n):
        union = set()
        for j in range(n):
            if (i >> j) & 1:
                union = union.union(subsets[j])
        if union not in subsets:
            subsets.append(union)

    return Topology(space, subsets)


def create_topology_from_equivalence(space, equivalence_relation):
    """
    Create a topology on the given space based on an equivalence relation.

    The open sets in this topology are defined as unions of equivalence classes.

    Parameters:
        space (set): The set on which the topology is defined.
        equivalence_relation (function): A function that takes two elements and returns True if they are equivalent.

    Returns:
        Topology: An instance of the Topology class representing the topology based on the equivalence relation.
    """
    # Find equivalence classes
    equivalence_classes = []
    visited = set()
    for element in space:
        if element not in visited:
            eq_class = {x for x in space if equivalence_relation(element, x)}
            equivalence_classes.append(eq_class)
            visited.update(eq_class)

    # Open sets are unions of equivalence classes, including the empty set
    subsets = [set()]
    n = len(equivalence_classes)
    for i in range(1, 2 ** n):
        union = set()
        for j in range(n):
            if (i >> j) & 1:
                union.update(equivalence_classes[j])
        subsets.append(union)

    return Topology(space, subsets)


def create_upward_closed_topology(space, order_relation):
    """
    Create a topology where open sets are upward-closed sets in a partial order.

    An **upward-closed set** contains, along with each of its elements, all elements greater than or equal to it in the given order.

    Parameters:
        space (set): The set on which the topology is defined.
        order_relation (dict): A mapping where order_relation[x] is a set of elements greater than or equal to x.

    Returns:
        Topology: An instance of the Topology class representing the upward-closed topology.
    """
    # Generate upward-closed sets
    subsets = [set(), set(space)]
    for element in space:
        upward_closed_set = order_relation[element]
        subsets.append(upward_closed_set)

    # Include unions of upward-closed sets
    n = len(subsets)
    for i in range(1, 2 ** n):
        union = set()
        for j in range(n):
            if (i >> j) & 1:
                union = union.union(subsets[j])
        if union not in subsets:
            subsets.append(union)

    return Topology(space, subsets)


def create_alexandrov_topology(space, order_relation):
    """
    Create the Alexandrov topology on the given space based on an order relation.

    The **Alexandrov topology** is a topology where arbitrary intersections of open sets are also open, making it particularly useful in domain theory.

    Parameters:
        space (set): The set on which the topology is defined.
        order_relation (function): A function that takes two elements \(x, y\) and returns True if \(x \leq y\).

    Returns:
        Topology: An instance of the Topology class representing the Alexandrov topology.
    """
    # For each element, find its upper set
    upper_sets = []
    for element in space:
        upper_set = {x for x in space if order_relation(element, x)}
        upper_sets.append(upper_set)

    # Open sets are arbitrary unions of upper sets, including the empty set
    subsets = [set()]
    n = len(upper_sets)
    for i in range(1, 2 ** n):
        union = set()
        for j in range(n):
            if (i >> j) & 1:
                union.update(upper_sets[j])
        if union not in subsets:
            subsets.append(union)

    # Ensure the whole space is included
    if set(space) not in subsets:
        subsets.append(set(space))

    return Topology(space, subsets)
