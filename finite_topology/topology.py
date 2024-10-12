from typing import Union, Callable
from itertools import permutations, combinations, chain


class Topology:
    """
    Represents a topology on a finite set.

    Class Attributes:
    - known_topologies (dict): Stores known topologies to facilitate identification.

    Instance Attributes:
    - space (set): The space on which the topology is defined.
    - collection_of_subsets (list): Collection of subsets that form the topology.
    """
    known_topologies = {}  # Class attribute to store known topologies

    def __init__(self, space, collection_of_subsets):
        """
        Initializes a topology with a given space and a collection of subsets.

        Parameters:
        space (iterable): The set representing the space.
        collection_of_subsets (iterable of iterables): The collection of subsets forming the topology.
        """
        self.space = set(space)
        # Ensure uniqueness of subsets
        unique_subsets = set(frozenset(s) for s in collection_of_subsets)
        self.collection_of_subsets = [set(s) for s in unique_subsets]

    def is_topology(self) -> bool:
        """
        Checks if the collection of subsets forms a topology on the given space.

        Returns:
        bool: True if the collection is a topology, False otherwise.
        """
        # Check if the empty set and the entire space are in the collection
        if set() not in self.collection_of_subsets:
            print("The empty set is not in the collection.")
            return False
        if self.space not in self.collection_of_subsets:
            print("The entire space is not in the collection.")
            return False

        n = len(self.collection_of_subsets)

        # Check if arbitrary unions of elements are in the collection
        for i in range(1, 2 ** n):
            union = set()
            for j in range(n):
                if (i >> j) & 1:
                    union = union.union(self.collection_of_subsets[j])
            if union not in self.collection_of_subsets:
                print(f"The union {union} is not in the collection.")
                return False

        # Check if finite intersections of elements are in the collection
        for i in range(1, 2 ** n):
            indices = [j for j in range(n) if (i >> j) & 1]
            if len(indices) <= 1:
                continue  # The intersection of a single set is the set itself
            intersection = self.collection_of_subsets[indices[0]]
            for idx in indices[1:]:
                intersection = intersection.intersection(self.collection_of_subsets[idx])
            if intersection not in self.collection_of_subsets:
                print(f"The intersection {intersection} is not in the collection.")
                return False

        return True

    def add_set(self, new_set) -> bool:
        """
        Adds a new set to the collection of subsets.

        Parameters:
        new_set (iterable): The new set to be added to the collection.

        Returns:
        bool: True if the new set is added successfully and the collection remains a topology, False otherwise.
        """
        new_set = set(new_set)
        if not new_set.issubset(self.space):
            print(f"The set {new_set} is not a subset of the space {self.space}. Cannot add.")
            return False

        if new_set not in self.collection_of_subsets:
            self.collection_of_subsets.append(new_set)
            print(f"Added the set {new_set} to the collection.")
            if self.is_open(new_set):
                print(f"The set {new_set} is open.")
            if self.is_closed(new_set):
                print(f"The set {new_set} is closed.")
        else:
            print(f"The set {new_set} is already in the collection.")

        # Verify if the collection is still a topology
        if self.is_topology():
            print("After adding, the collection is still a topology.")
            return True
        else:
            print("After adding, the collection is no longer a topology.")
            return False

    def get_ordered_subsets(self) -> list:
        """
        Returns the collection of subsets aesthetically ordered.

        Returns:
        List[Set]: List of subsets ordered by the specified criterion.
        """
        # Separate the entire space and the empty set
        space_set = self.space
        empty_set = set()

        subsets = self.collection_of_subsets.copy()

        # Remove the entire space and the empty set from the temporary list
        subsets = [s for s in subsets if s != space_set and s != empty_set]

        # Sort the subsets by size (ascending order)
        subsets.sort(key=lambda s: len(s))

        # Create the ordered list: first the space, then the empty set, then the subsets ordered by size
        ordered_subsets = [space_set, empty_set] + subsets

        return ordered_subsets

    def __repr__(self) -> str:
        """
        Returns a string representation of the Topology instance.

        Returns:
        str: String representation of the topology.
        """
        id_str = "Topology" if self.is_topology() else "Set"
        ordered_subsets = self.get_ordered_subsets()

        # Build the string representation
        subsets_str = "\n    ".join(str(sorted(s)) for s in ordered_subsets)

        return (f"{id_str}(\n"
                f"  Space: {sorted(self.space)},\n"
                f"  Collection of Subsets:\n"
                f"    {subsets_str}\n)")

    def __len__(self) -> int:
        """
        Returns the number of subsets in the collection.

        Returns:
        int: Number of subsets.
        """
        return len(self.collection_of_subsets)

    def __eq__(self, other) -> bool:
        """
        Compares two topologies for structural equality.

        Parameters:
        other (Topology): Another topology to compare.

        Returns:
        bool: True if the topologies are structurally equal, False otherwise.
        """
        return self.is_structurally_equal(other)

    def is_structurally_equal(self, other: 'Topology') -> bool:
        """
        Checks if two topologies have the same structure, regardless of the elements.

        Parameters:
        other (Topology): Another topology to compare.

        Returns:
        bool: True if the topologies have the same structure, False otherwise.
        """
        if not isinstance(other, Topology):
            return False

        # Check if the sizes of the spaces are equal
        if len(self.space) != len(other.space):
            return False

        # Check if the number of subsets is equal
        if len(self.collection_of_subsets) != len(other.collection_of_subsets):
            return False

        # Map elements to indices
        self_elements = list(self.space)
        other_elements = list(other.space)

        # Generate all possible bijections between the two spaces
        for perm in permutations(other_elements):
            mapping = dict(zip(self_elements, perm))

            # Apply mapping to all subsets in self.collection_of_subsets
            mapped_subsets = [set(mapping[e] for e in subset) for subset in self.collection_of_subsets]

            # Compare the mapped subsets with the collection of subsets of the other
            if set(frozenset(s) for s in mapped_subsets) == set(frozenset(s) for s in other.collection_of_subsets):
                return True

        return False

    def identify_topology(self, known_topologies) -> list:
        """
        Identifies the topology by comparing it to a list of known topologies.

        Parameters:
        known_topologies (dict): A dictionary with names as keys and Topology objects as values.

        Returns:
        list: Names of known topologies that are homeomorphic to this topology.
        """
        matches = []
        for name, known_topo in known_topologies.items():
            if self.is_structurally_equal(known_topo):
                matches.append(name)
        return matches

    def get_basis(self) -> list:
        """
        Computes and returns a basis for the topology.

        A **basis** for a topology :math:`\\tau` on a set :math:`X` is a collection of open sets :math:`\\mathcal{B}` such that every open set in :math:`\\tau` can be written as a union of sets in :math:`\\mathcal{B}`.

        .. math::

            \\forall U \\in \\tau, \\quad \\exists \\{ B_i \\}_{i \\in I} \\subseteq \\mathcal{B}, \\quad U = \\bigcup_{i \\in I} B_i

        Returns:
            list[set]: A list of sets representing the basis of the topology.
        """
        basis = []

        # Exclude the empty set if desired, as it is usually not included in the basis
        open_sets = [s for s in self.collection_of_subsets if s]

        for open_set in open_sets:
            # Check if open_set can be expressed as a union of other open sets
            can_be_formed = False
            for i in range(1, len(open_sets) + 1):
                for subsets in combinations(open_sets, i):
                    if open_set in subsets:
                        continue  # Skip if open_set is in the combination
                    union_subsets = set().union(*subsets)
                    if union_subsets == open_set:
                        can_be_formed = True
                        break
                if can_be_formed:
                    break
            if not can_be_formed:
                basis.append(open_set)

        return basis

    def is_discrete(self) -> bool:
        """
        Checks if the topology is discrete.

        A **discrete topology** on a set :math:`X` is the topology in which every subset of :math:`X` is open.
        This means the topology :math:`\\tau` is equal to the power set of :math:`X`.

        .. math::

            \\tau = \\mathcal{P}(X)

        Returns:
            bool: True if the topology is discrete, False otherwise.
        """
        # Ensure the collection of subsets forms a valid topology
        if not self.is_topology():
            return False

        # Generate the power set of the space (all possible subsets)
        all_subsets = [set(s) for s in chain.from_iterable(combinations(self.space, r) for r in range(len(self.space) + 1))]

        # Convert both to sets of frozensets for precise comparison
        power_set = set(frozenset(s) for s in all_subsets)
        topology_set = set(frozenset(s) for s in self.collection_of_subsets)

        # Check if the collection of subsets matches the power set
        return topology_set == power_set

    def is_connected(self) -> bool:
        """
        Checks if the topological space is connected.

        A topological space :math:`(X, \\tau)` is **connected** if it cannot be represented as the union of two disjoint non-empty open sets.

        .. math::

            \\text{A space is connected if } \\nexists U, V \\in \\tau, \\quad U \\cap V = \\emptyset, \\; U \\cup V = X, \\; U \\neq \\emptyset, \\; V \\neq \\emptyset

        Returns:
            bool: True if the space is connected, False otherwise.
        """
        # An empty space or a space with a single point is connected
        if len(self.space) <= 1:
            return True

        # Generate all possible partitions of the space into two non-empty sets
        space_list = list(self.space)
        n = len(space_list)

        # Iterate over all combinations for the first set
        for r in range(1, n // 2 + 1):
            for subset in combinations(space_list, r):
                U = set(subset)
                V = self.space - U

                # Check if U and V are open
                if U in self.collection_of_subsets and V in self.collection_of_subsets:
                    # Found a partition that separates the space, it is not connected
                    print(f"Space separated into U={sorted(U)} and V={sorted(V)}.")
                    return False

        return True

    @staticmethod
    def is_compact() -> bool:
        """
        Checks if the topological space is compact.

        A topological space is **compact** if every open cover has a finite subcover.
        Formally, given an open cover of the space, which is a collection of open sets whose union contains the entire space,
        there exists a finite subcollection that also covers the entire space.

        Definitions:

        - **Open Cover**: An open cover of a set :math:`X` in a topological space :math:`(X, \\tau)` is a collection of open sets :math:`\\{U_i\\}_{i \\in I}` such that the union of all :math:`U_i` contains the set :math:`X`:

          .. math::

            X \\subseteq \\bigcup_{i \\in I} U_i

        - **Subcover**: A subcover is a subcollection of the open cover that still covers the set :math:`X`. In other words, if :math:`\\{U_i\\}_{i \\in I}` is an open cover of :math:`X`, a **subcover** is a subcollection :math:`\\{U_j\\}_{j \\in J}`, where :math:`J \\subseteq I`, such that:

          .. math::

            X \\subseteq \\bigcup_{j \\in J} U_j

        Returns:
            bool: True if the space is compact, False otherwise.
        """
        # In finite spaces, all topological spaces are compact
        return True

    def is_open(self, subset: set) -> bool:
        """
        Checks if the given subset is open in the topological space.

        Parameters:
        subset (set): The set to be checked.

        Returns:
        bool: True if the subset is open, False otherwise.
        """
        if subset in self.collection_of_subsets:
            return True
        else:
            print(f"The set {sorted(subset)} is not open.")
            return False

    def is_closed(self, subset: set) -> bool:
        """
        Checks if the given subset is closed in the topological space.

        A set is **closed** if its complement is open.

        Parameters:
        subset (set): The set to be checked.

        Returns:
        bool: True if the subset is closed, False otherwise.
        """
        complement = self.space - subset
        if complement in self.collection_of_subsets:
            return True
        else:
            print(f"The set {sorted(subset)} is not closed.")
            return False

    def get_complement(self, subset: set) -> set:
        """
        Returns the complement of the given subset in the topological space.

        The **complement** of a set \(A\) in a topological space \(X\) is the set of elements in \(X\) that are not in \(A\).

        .. math::

            \\text{Complement}(A) = X \\setminus A

        Parameters:
        subset (set): The subset for which the complement is to be obtained.

        Returns:
        set: The complement of the subset in the topological space.
        """
        if not subset.issubset(self.space):
            raise ValueError(f"The set {subset} is not a subset of the space {self.space}.")
        return self.space - subset

    def find_dense_subset(self) -> set:
        """
        Finds and returns a dense subset of the topological space.

        A **dense subset** of a topological space :math:`(X, \\tau)` is a subset :math:`A \\subseteq X` such that the closure of :math:`A` is equal to :math:`X`.
        In other words, :math:`A` is dense if every point in :math:`X` is either in :math:`A` or is a limit point of :math:`A`.

        .. math::

            A \\text{ is dense in } X \\text{ if } \\overline{A} = X

        Returns:
            set: A dense subset if it exists, otherwise the entire space if it is the only dense subset (trivial case).
        """
        dense_subsets = []

        # In finite spaces, find the smallest subset whose closure is the entire space
        for r in range(1, len(self.space) + 1):
            for subset in combinations(self.space, r):
                closure = self.get_closure(set(subset))
                if closure == self.space:
                    dense_subsets.append(set(subset))

        # If the only dense subset is the entire space, return it with a note that it's trivial
        if len(dense_subsets) == 1 and dense_subsets[0] == self.space:
            print("The only dense subset is the entire space, which is a trivial case in finite topologies.")
            return self.space

        # Return the smallest non-trivial dense subset
        if dense_subsets:
            return min(dense_subsets, key=len)

        return set()

    @staticmethod
    def create_alexandrov_topology(space: set,
                                   order_relation: Union[Callable[[int, int], bool], dict],
                                   # La función toma dos enteros y retorna un booleano
                                   relation_type: str = 'function') -> 'Topology':
        """
        Creates the Alexandrov topology on the given space based on an order relation.

        The **Alexandrov topology** is a topology where every intersection of open sets is also open. It is commonly used in domain theory and theoretical computer science.

        Parameters:
            space (set): The set on which the topology is defined.
            order_relation (function or dict):
                - If `relation_type` is 'function': A function that takes two elements :math:`x, y` and returns True if :math:`x \\leq y`.
                - If `relation_type` is 'dict': A dictionary where :math:`\\text{order_relation}[x]` is a set of elements greater than or equal to :math:`x`.

            relation_type (str): Specifies the type of `order_relation` ('function' or 'dict').

        Returns:
            Topology: An instance of the Topology class representing the Alexandrov topology.

        Example:
            If the space is :math:`\\{a, b, c\\}` and the order relation is given by :math:`a \\leq b` and :math:`b \\leq c`, the Alexandrov topology will include sets that respect this order relation.

        .. math::

            \\forall x, y \\in X, \\quad U \\cap V \\in \\tau \\quad \\text{for all } U, V \\in \\tau
        """
        if relation_type == 'function':
            # Generate upper sets using the relation function
            upper_sets = []
            for element in space:
                upper_set = {x for x in space if order_relation(element, x)}
                upper_sets.append(upper_set)
        elif relation_type == 'dict':
            # Assume that order_relation[x] is the upper set for x
            upper_sets = list(order_relation.values())
        else:
            raise ValueError("relation_type must be 'function' or 'dict'.")

        # Open sets are all unions of upper sets, including the empty set
        subsets = [set()]  # Start with the empty set
        n = len(upper_sets)
        for i in range(1, 2 ** n):
            union = set()
            for j in range(n):
                if (i >> j) & 1:
                    union = union.union(upper_sets[j])
            if union not in subsets:
                subsets.append(union)

        # Ensure the entire space is included
        if set(space) not in subsets:
            subsets.append(set(space))

        return Topology(space, subsets)

    def is_separable(self) -> bool:
        """
        Checks if the topological space is separable.

        A **separable space** is one that contains a countable, dense subset.

        .. note::

            In finite topological spaces, any non-empty subset can be considered dense if its closure is the entire space.

        Returns:
            bool: True if the space is separable, False otherwise.
        """
        # In finite spaces, all spaces are separable
        if len(self.space) <= 1:
            return True

        # In finite spaces, any non-empty finite set can be a dense basis if its closure is the entire space
        for r in range(1, len(self.space) + 1):
            for subset in combinations(self.space, r):
                closure = self.get_closure(set(subset))
                if closure == self.space:
                    return True
        return False

    def get_closure(self, subset: set) -> set:
        """
        Obtains the exterior of a given set in the topological space.

        The **exterior** of a set :math:`A` in a topological space :math:`(X, \\tau)` is defined as the interior of its complement.

        .. math::

            \\text{Exterior}(A) = \\text{Interior}(X \\setminus A)

        Parameters:
            subset (set): The set for which the exterior is to be obtained.

        Returns:
            set: The exterior of the set.
        """
        # Define closed sets as complements of open sets
        closed_sets = [self.space - open_set for open_set in self.collection_of_subsets]

        # Initialize closure as the entire space
        closure = self.space.copy()

        # Intersect all closed sets that contain 'subset'
        for closed_set in closed_sets:
            if subset.issubset(closed_set):
                closure = closure.intersection(closed_set)

        return closure

    def is_hausdorff(self) -> bool:
        """
        Checks if the topological space is Hausdorff (T2).

        A topological space :math:`(X, \\tau)` is **Hausdorff** if, for any two distinct points, there exist disjoint open sets containing each of the points.

        .. math::

            \\forall x, y \\in X, \\quad x \\neq y \\implies \\exists U, V \\in \\tau, \\quad x \\in U, \\quad y \\in V, \\quad U \\cap V = \\emptyset

        Returns:
            bool: True if the space is Hausdorff, False otherwise.
        """
        # Iterate over all pairs of distinct points
        for x, y in combinations(self.space, 2):
            separated = False
            # Find pairs of open sets that separate x and y
            for U in self.collection_of_subsets:
                if x in U:
                    for V in self.collection_of_subsets:
                        if y in V and U.isdisjoint(V):
                            separated = True
                            break
                if separated:
                    break
            if not separated:
                print(f"Cannot separate points {x} and {y} with disjoint open sets.")
                return False
        return True

    def get_interior(self, subset: set) -> set:
        """
        Obtains the interior of a given set in the topological space.

        The **interior** of a set :math:`A` in a topological space :math:`(X, \\tau)` is the largest open set contained within :math:`A`. Formally:

        .. math::

            \\text{Interior}(A) = \\bigcup \\{ U \\in \\tau : U \\subseteq A \\}

        Parameters:
            subset (set): The set for which the interior is to be obtained.

        Returns:
            set: The interior of the set.
        """
        interior = set()
        for open_set in self.collection_of_subsets:
            if open_set.issubset(subset):
                interior = interior.union(open_set)
        return interior

    def get_boundary(self, subset: set) -> set:
        """
        Obtains the boundary of a given set in the topological space.

        The **boundary** of a set :math:`A` in a topological space :math:`(X, \\tau)` is defined as the difference between the closure and the interior of :math:`A`. Formally:

        .. math::

            \\partial A = \\overline{A} \\setminus \\text{Interior}(A)

        Parameters:
            subset (set): The set for which the boundary is to be obtained.

        Returns:
            set: The boundary of the set.
        """
        closure = self.get_closure(subset)
        interior = self.get_interior(subset)
        boundary = closure - interior
        return boundary

    def get_exterior(self, subset: set) -> set:
        """
        Obtains the exterior of a given set in the topological space.

        The **exterior** of a set :math:`A` in a topological space :math:`(X, \\tau)` is defined as the interior of its complement.

        .. math::

            \\text{Exterior}(A) = \\text{Interior}(X \\setminus A)

        Parameters:
            subset (set): The set for which the exterior is to be obtained.

        Returns:
            set: The exterior of the set.
        """
        complement = self.space - subset
        exterior = self.get_interior(complement)
        return exterior

    def is_T0(self) -> bool:
        """
        Checks if the topological space is T0.

        In a T0 space (Kolmogorov space), for every pair of distinct points, there exists an open set containing one of the points but not the other.

        .. math::

            \\forall x, y \\in X, \\quad x \\neq y \\implies \\exists U \\in \\tau, \\quad (x \\in U \\wedge y \\notin U) \\text{ or } (y \\in U \\wedge x \\notin U)

        Returns:
            bool: True if the space is T0, False otherwise.
        """
        # Iterate over all pairs of distinct points
        for x, y in combinations(self.space, 2):
            # Check if at least one can be separated from the other
            x_separates = any(x in U and y not in U for U in self.collection_of_subsets)
            y_separates = any(y in U and x not in U for U in self.collection_of_subsets)

            if not (x_separates or y_separates):
                print(f"Cannot separate {x} and {y} in a T0 space.")
                return False
        return True

    def is_T1(self) -> bool:
        """
        Checks if the topological space is T1.

        A topological space :math:`(X, \\tau)` is **T1** if, for every pair of distinct points,
        each has a neighborhood that does not contain the other.

        Additionally, in a T1 space, every single point must be closed, meaning
        its complement is an open set.

        .. math::

            \\forall x, y \\in X, \\quad x \\neq y \\implies \\exists U, V \\in \\tau, \\quad
            (x \\in U \\wedge y \\notin U) \\wedge (y \\in V \\wedge x \\notin V)

        Returns:
            bool: True if the space is T1, False otherwise.
        """
        # Iterate over all points in the space
        for point in self.space:
            # Calculate the complement of the current point
            complement = self.space - {point}

            # Check if the complement is an open set
            if complement not in self.collection_of_subsets:
                print(f"Point {point} is not closed, complement {complement} is not open.")
                return False

        # If all points are closed (i.e., their complements are open), the space is T1
        return True
