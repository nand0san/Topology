from itertools import chain, combinations
from typing import Set, Any, Callable, Dict, List, Union
from .topology import Topology
import logging

logger = logging.getLogger(__name__)


def create_discrete_topology(space: Set[Any]) -> Topology:
    r"""
    Create a discrete topology on the given space.

    A **discrete topology** on a set :math:`X` is the topology in which every subset of :math:`X` is open. This means that the topology :math:`\tau` is equal to the power set of :math:`X`.

    .. math::

        \tau = \mathcal{P}(X)

    Example:
        A function from any space with a discrete topology to any other topology is continuous.

    Parameters:
        space (set): The set over which the discrete topology is defined.

    Returns:
        Topology: An instance of the Topology class representing the discrete topology.
    """
    # Generar todos los subconjuntos posibles (el conjunto potencia)
    subsets = list(chain.from_iterable(combinations(space, r) for r in range(len(space) + 1)))
    subsets = [set(s) for s in subsets]
    logger.debug(f"Subconjuntos generados para la topología discreta: {subsets}")
    return Topology(collection_of_subsets=subsets, generate=False)


def create_indiscrete_topology(space: Set[Any]) -> Topology:
    r"""
    Create the indiscrete (trivial) topology on the given space.

    An **indiscrete topology** (also known as the **trivial topology**) on a set :math:`X` contains only the empty set and the entire set.

    .. math::

        \tau = \{ \emptyset, X \}

    Example:
        A function to any space with an indiscrete topology is always continuous.

    Parameters:
        space (set): The set over which the indiscrete topology is defined.

    Returns:
        Topology: An instance of the Topology class representing the indiscrete topology.
    """
    subsets = [set(), set(space)]
    logger.debug(f"Subconjuntos generados para la topología indiscreta: {subsets}")
    return Topology(collection_of_subsets=subsets, generate=False)


def create_sierpinski_topology() -> Topology:
    r"""
    Create the Sierpiński topology.

    The **Sierpiński topology** is defined on the set :math:`\{0, 1\}` with the collection of open sets being :math:`\{ \emptyset, \{1\}, \{0, 1\} \}`.

    Example:
        The Sierpiński topology is important in domain theory and theoretical computer science.

    Returns:
        Topology: An instance of the Topology class representing the Sierpiński topology.
    """
    space = {0, 1}
    subsets = [set(), {1}, set(space)]
    logger.debug(f"Subconjuntos generados para la topología de Sierpiński: {subsets}")
    return Topology(collection_of_subsets=subsets, generate=False)


def create_particular_point_topology(space: Set[Any], particular_point: Any) -> Topology:
    r"""
     Create a particular point topology on the given space.

     A **particular point topology** on a set :math:`X` is defined so that every non-empty open set must include a distinguished point :math:`p \in X`.

     Example:
         In a particular point topology, the only continuous functions are those that are constant or map the distinguished point to any open set.

     Parameters:
         space (set): The set over which the particular point topology is defined.
         particular_point (Any): The distinguished point that must be included in all non-empty open sets.

     Returns:
         Topology: An instance of the Topology class representing the particular point topology.

     Raises:
         ValueError: If the particular point is not an element of the space.
     """
    if particular_point not in space:
        raise ValueError("El punto particular debe ser un elemento del espacio.")

    # Todos los subconjuntos que contienen el punto particular, más el conjunto vacío
    subsets = [set(), set(space)]
    for r in range(1, len(space)):
        for subset in combinations(space, r):
            subset_set = set(subset)
            if particular_point in subset_set:
                subsets.append(subset_set)
    logger.debug(f"Subconjuntos generados para la topología de punto particular: {subsets}")
    return Topology(collection_of_subsets=subsets, generate=False)


def create_excluded_point_topology(space: Set[Any], excluded_point: Any) -> Topology:
    r"""
    Create an excluded point topology on the given space.

    An **excluded point topology** on a set :math:`X` is defined so that the only open sets are those that do not contain a particular point :math:`e \in X`, along with the entire set and the empty set.

    Parameters:
        space (set): The set over which the excluded point topology is defined.
        excluded_point (Any): The point that is excluded from all non-empty open sets.

    Returns:
        Topology: An instance of the Topology class representing the excluded point topology.

    Raises:
        ValueError: If the excluded point is not an element of the space.
    """
    if excluded_point not in space:
        raise ValueError("El punto excluido debe ser un elemento del espacio.")

    # Todos los subconjuntos que no contienen el punto excluido, más el conjunto completo y el conjunto vacío
    subsets = [set(), set(space)]
    for r in range(1, len(space)):
        for subset in combinations(space, r):
            subset_set = set(subset)
            if excluded_point not in subset_set:
                subsets.append(subset_set)
    logger.debug(f"Subconjuntos generados para la topología de punto excluido: {subsets}")
    return Topology(collection_of_subsets=subsets, generate=False)


def create_divisibility_topology(space: Set[int]) -> Topology:
    r"""
    Create a divisibility topology on the given space.

    A **divisibility topology** on a set of integers is defined so that the basic open sets are all multiples of each element in the space. Specifically, for each element :math:`n` in the space, the set of all multiples of :math:`n` within the space is considered an open set.

    Example:
        Consider the set :math:`\{1, 2, 3\}`. The divisibility topology would include:
        - :math:`\emptyset`
        - :math:`\{1, 2, 3\}` (all multiples of 1)
        - :math:`\{2\}` (multiples of 2)
        - :math:`\{3\}` (multiples of 3)
        - Any union of these sets, such as :math:`\{1, 2\}`, :math:`\{1, 3\}`, etc.

    Parameters:
        space (set): The set over which the divisibility topology is defined. Expected to contain integers.

    Returns:
        Topology: An instance of the Topology class representing the divisibility topology.
    """
    subsets: Set[frozenset[int]] = {frozenset(), frozenset(space)}

    for element in space:
        if element == 0:
            # Evitar división por cero
            multiples = {0}
            logger.debug(f"Elemento 0 encontrado. Múltiplos: {multiples}")
        else:
            multiples = {x for x in space if isinstance(x, int) and x % element == 0}
            logger.debug(f"Múltiplos de {element}: {multiples}")
        subsets.add(frozenset(multiples))

    # Convertir el conjunto a lista para indexación
    subsets_list: List[frozenset[int]] = list(subsets)

    # Asegurar que la topología esté cerrada bajo uniones arbitrarias
    # Para simplicidad en casos finitos, incluir todas las uniones de los conjuntos abiertos básicos
    n = len(subsets_list)
    for i in range(1, 2 ** n):
        union = set()
        for j in range(n):
            if (i >> j) & 1:
                union = union.union(subsets_list[j])
        union_frozen = frozenset(union)
        if union_frozen not in subsets:
            subsets.add(union_frozen)
            subsets_list.append(union_frozen)
            logger.debug(f"Unión añadida: {union_frozen}")

    # Convertir de vuelta a lista de sets
    final_subsets: List[Set[int]] = [set(s) for s in subsets]

    logger.debug(f"Subconjuntos finales para la topología de divisibilidad: {final_subsets}")
    return Topology(collection_of_subsets=final_subsets, generate=False)


def create_topology_from_equivalence(space: Set[Any], equivalence_relation: Callable[[Any, Any], bool]) -> Topology:
    r"""
    Create a topology on the given space based on an equivalence relation.

    The topology on this space is defined such that the open sets are the unions of equivalence classes.

    Parameters:
        space (set): The set over which the topology is defined.
        equivalence_relation (Callable[[Any, Any], bool]): A function that takes two elements and returns True if they are equivalent.

    Returns:
        Topology: An instance of the Topology class representing the topology based on the equivalence relation.
    """
    # Encontrar clases de equivalencia
    equivalence_classes: List[Set[Any]] = []
    visited: Set[Any] = set()
    for element in space:
        if element not in visited:
            eq_class = {x for x in space if equivalence_relation(element, x)}
            equivalence_classes.append(eq_class)
            visited.update(eq_class)
            logger.debug(f"Clase de equivalencia encontrada: {eq_class}")

    # Los conjuntos abiertos son las uniones de las clases de equivalencia, incluyendo el conjunto vacío
    subsets: Set[frozenset[Any]] = {frozenset()}
    n = len(equivalence_classes)
    for i in range(1, 2 ** n):
        union = set()
        for j in range(n):
            if (i >> j) & 1:
                union.update(equivalence_classes[j])
        subsets.add(frozenset(union))
        logger.debug(f"Unión de clases de equivalencia añadida: {union}")

    # Convertir a lista de sets
    final_subsets: List[Set[Any]] = [set(s) for s in subsets]

    return Topology(collection_of_subsets=final_subsets, generate=False)


def create_upward_closed_topology(space: Set[Any], order_relation: Callable[[Any, Any], bool]) -> Topology:
    r"""
    Create a topology where open sets are upward-closed sets in a partial order.

    An **upward-closed topology** (or **upper sets**) contains, along with each of its elements, all greater or equal elements according to the given order relation.

    This type of topology is useful in order theory and domain theory, particularly in theoretical computer science and lattice theory.

    Example:
        Consider the set :math:`\{1, 2, 3\}` with the usual ordering of integers. In this case, the upward-closed sets would be:
        - :math:`\emptyset`
        - :math:`\{1, 2, 3\}` (starting from 1)
        - :math:`\{2, 3\}` (starting from 2)
        - :math:`\{3\}` (starting from 3)

    Parameters:
        space (set): The set over which the topology is defined.
        order_relation (Callable[[Any, Any], bool]): A function that takes two elements :math:`x, y` and returns True if :math:`x \leq y`.

    Returns:
        Topology: An instance of the Topology class representing the upward-closed topology.
    """
    # Generar conjuntos ascendentes
    upper_sets: List[Set[Any]] = []
    for element in space:
        upper_set = {x for x in space if order_relation(element, x)}
        upper_sets.append(upper_set)
        logger.debug(f"Conjunto ascendente generado para {element}: {upper_set}")

    # Los conjuntos abiertos son las uniones arbitrarias de conjuntos ascendentes, incluyendo el conjunto vacío
    subsets: Set[frozenset[Any]] = {frozenset()}
    n = len(upper_sets)
    for i in range(1, 2 ** n):
        union = set()
        for j in range(n):
            if (i >> j) & 1:
                union = union.union(upper_sets[j])
        subsets.add(frozenset(union))
        logger.debug(f"Unión de conjuntos ascendentes añadida: {union}")

    # Asegurar que el conjunto completo esté incluido
    subsets.add(frozenset(space))

    # Convertir a lista de sets
    final_subsets: List[Set[Any]] = [set(s) for s in subsets]

    return Topology(collection_of_subsets=final_subsets, generate=False)


def create_alexandrov_topology(
        space: Set[Any],
        order_relation: Union[Callable[[Any, Any], bool], Dict[Any, Set[Any]]],
        relation_type: str = 'function'
) -> Topology:
    """
    Create the Alexandrov topology on the given space based on an order relation.

    The **Alexandrov topology** is a topology where arbitrary intersections of open sets are also open.
    This topology is commonly used in domain theory and order theory.

    In the Alexandrov topology, for each element :math:`x` in the space, the "upward set" that contains
    all elements greater than or equal to :math:`x` (according to the order relation) forms an open set.

    Example:
        Consider the set :math:`\\{a, b, c\\}` with the following order relation:

        - :math:`a \\leq b`
        - :math:`b \\leq c`

        The upward sets would be:

        - :math:`\\{a, b, c\\}` (starting from :math:`a`)
        - :math:`\\{b, c\\}` (starting from :math:`b`)
        - :math:`\\{c\\}` (starting from :math:`c`)

        In this example, the open sets in the Alexandrov topology are the arbitrary unions of these upward sets,
        along with the empty set.

    Parameters:
        space (set): The set over which the topology is defined.
        order_relation (Callable[[Any, Any], bool] or Dict[Any, Set[Any]]):
            - If `relation_type` is 'function': A function that takes two elements :math:`x, y` and returns True if :math:`x \\leq y`.
            - If `relation_type` is 'dict': A dictionary where `order_relation[x]` is a set of elements greater than or equal to `x`.
        relation_type (str): Specifies the type of `order_relation` ('function' or 'dict').

    Returns:
        Topology: An instance of the Topology class representing the Alexandrov topology.

    .. math::

        \\forall x, y \\in X, \\quad U \\cap V \\in \\tau \\quad \\text{for all } U, V \\in \\tau
    """
    if relation_type == 'function':
        # Generar conjuntos ascendentes usando la función de relación
        upper_sets: List[Set[Any]] = []
        for element in space:
            upper_set = {x for x in space if order_relation(element, x)}
            upper_sets.append(upper_set)
            logger.debug(f"Conjunto ascendente generado para {element}: {upper_set}")
    elif relation_type == 'dict':
        # Asumir que order_relation[x] es el conjunto ascendente para x
        upper_sets = list(order_relation.values())
        logger.debug(f"Conjuntos ascendentes extraídos del diccionario: {upper_sets}")
    else:
        raise ValueError("relation_type debe ser 'function' o 'dict'.")

    # Los conjuntos abiertos son las uniones arbitrarias de conjuntos ascendentes, incluyendo el conjunto vacío
    subsets: Set[frozenset[Any]] = {frozenset()}
    n = len(upper_sets)
    for i in range(1, 2 ** n):
        union = set()
        for j in range(n):
            if (i >> j) & 1:
                union = union.union(upper_sets[j])
        subsets.add(frozenset(union))
        logger.debug(f"Unión de conjuntos ascendentes añadida: {union}")

    # Asegurar que el conjunto completo esté incluido
    subsets.add(frozenset(space))

    # Convertir a lista de sets
    final_subsets: List[Set[Any]] = [set(s) for s in subsets]

    return Topology(collection_of_subsets=final_subsets, generate=False)
