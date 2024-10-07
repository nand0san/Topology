from itertools import permutations, combinations



class Topology:
    known_topologies = {}  # Class attribute to store known topologies

    def __init__(self, space, collection_of_subsets):
        self.space = set(space)
        self.collection_of_subsets = [set(s) for s in collection_of_subsets]

    def is_topology(self):
        """
        Check if the collection of subsets forms a topology on the given space.

        Returns:
        bool: True if the collection is a topology, False otherwise.
        """
        # Check that the empty set and the total space are in the collection
        if set() not in self.collection_of_subsets:
            print("The empty set is not in the collection.")
            return False
        if self.space not in self.collection_of_subsets:
            print("The total space is not in the collection.")
            return False

        n = len(self.collection_of_subsets)

        # Check that arbitrary unions of elements are in the collection
        for i in range(1, 2 ** n):
            union = set()
            for j in range(n):
                if (i >> j) & 1:
                    union = union.union(self.collection_of_subsets[j])
            if union not in self.collection_of_subsets:
                print(f"The union {union} is not in the collection.")
                return False

        # Check that finite intersections of elements are in the collection
        for i in range(1, 2 ** n):
            indices = [j for j in range(n) if (i >> j) & 1]
            if len(indices) <= 1:
                continue  # The intersection of a single set is itself
            intersection = self.collection_of_subsets[indices[0]]
            for idx in indices[1:]:
                intersection = intersection.intersection(self.collection_of_subsets[idx])
            if intersection not in self.collection_of_subsets:
                print(f"The intersection {intersection} is not in the collection.")
                return False

        # If all checks pass
        print("The collection is a topology.")
        return True

    def add_set(self, new_set):
        """
        Add a new set to the collection of subsets.

        Parameters:
        new_set (iterable): The new set to be added to the collection.

        Returns:
        bool: True if the new set is added successfully and the collection remains a topology, False otherwise.
        """
        new_set = set(new_set)
        if not new_set.issubset(self.space):
            print(f"Set {new_set} is not a subset of the space {self.space}. Cannot add.")
            return False

        if new_set not in self.collection_of_subsets:
            self.collection_of_subsets.append(new_set)
            print(f"Added set {new_set} to the collection.")
        else:
            print(f"Set {new_set} is already in the collection.")

        # Check if the collection is still a topology
        if self.is_topology():
            print("After adding, the collection remains a topology.")
            return True
        else:
            print("After adding, the collection is no longer a topology.")
            return False

    def __repr__(self):
        return (f"Topology(\n"
                f"  Space: {self.space},\n"
                f"  Collection of Subsets:\n"
                f"    {self.collection_of_subsets}\n)")

    def __len__(self):
        """
        Return the number of subsets in the collection.
        """
        return len(self.collection_of_subsets)

    def is_structurally_equal(self, other):
        """
        Check if two topologies have the same structure, regardless of the elements.

        Parameters:
        other (Topology): Another topology to compare with.

        Returns:
        bool: True if the topologies have the same structure, False otherwise.
        """
        if not isinstance(other, Topology):
            return False

        # Check that the sizes of the spaces are equal
        if len(self.space) != len(other.space):
            return False

        # Check that the number of subsets is equal
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

            # Compare mapped subsets to other's collection of subsets
            if set(frozenset(s) for s in mapped_subsets) == set(frozenset(s) for s in other.collection_of_subsets):
                return True

        # If no bijection yields equality, the structures are not the same
        return False

    def identify_topology(self, known_topologies):
        """
        Identify the topology by comparing it to a list of known topologies.

        Parameters:
        known_topologies (dict): A dictionary with names as keys and Topology instances as values.

        Returns:
        list: Names of known topologies that are homeomorphic to this topology.
        """
        matches = []
        for name, known_topo in known_topologies.items():
            if self.is_structurally_equal(known_topo):
                matches.append(name)
        return matches

    def get_basis(self):
        """
        Compute and return a basis for the topology.

        Returns:
        List[Set]: A list of sets representing the basis of the topology.
        """
        basis = []

        # Exclude the empty set if desired, since it's usually not included in the basis
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
