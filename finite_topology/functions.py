# from itertools import permutations, combinations, chain
from .topology import Topology


class Function:
    """
    Represents a function between two topological spaces. It can be continous or not.

    Attributes:
    - source (Topology): The topological space from which the function originates.
    - target (Topology): The topological space to which the function maps.
    - mapping (dict): A dictionary mapping elements from the source space to the target space.
    """

    def __init__(self, source: Topology, target: Topology, mapping: dict):
        """
        Initializes a function between two topological spaces.

        Parameters:
        source (Topology): The source topological space.
        target (Topology): The target topological space.
        mapping (dict): A dictionary mapping elements from source.space to target.space.

        Raises:
        TypeError: If source or target are not instances of Topology.
        ValueError: If the mapping is not completely defined or contains elements not belonging to the spaces.
        """
        # Verify that source and target are instances of Topology
        if not isinstance(source, Topology):
            raise TypeError("The 'source' parameter must be an instance of Topology.")
        if not isinstance(target, Topology):
            raise TypeError("The 'target' parameter must be an instance of Topology.")

        # Verify that the mapping is completely defined
        if set(mapping.keys()) != source.space:
            raise ValueError("The mapping must be defined for all elements of the source space.")

        # Verify that the values of the mapping belong to the target space
        if not set(mapping.values()).issubset(target.space):
            raise ValueError("All values in the mapping must belong to the target space.")

        self.source = source
        self.target = target
        self.mapping = mapping

    def is_continuous(self) -> bool:
        """
        Checks if the function is continuous.

        A function between two topological spaces is **continuous** if the preimage of every open set in the target space is open in the source space.

        Returns:
        bool: True if the function is continuous, False otherwise.
        """
        # For each open set in the target space, verify that the preimage is open in the source space
        for open_set in self.target.collection_of_subsets:
            # Calculate the preimage
            preimage = self.get_preimage(open_set)
            # Verify if the preimage is open in the source space
            if preimage not in self.source.collection_of_subsets:
                print(f"The preimage of {sorted(open_set)} is {sorted(preimage)}, which is not an open set in the source space.")
                return False
        # If all preimages are open, the function is continuous
        return True

    def get_preimage(self, subset: set) -> set:
        """
        Obtains the preimage (inverse image) of a given set in the target space.

        Parameters:
        subset (set): A subset of the target space.

        Returns:
        set: The preimage of 'subset' in the source space.
        """
        return {x for x in self.source.space if self.mapping.get(x) in subset}

    def is_bijective(self) -> bool:
        """
        Checks if the function is bijective.

        A function is **bijective** if it is both injective (one-to-one) and surjective (onto).

        Returns:
        bool: True if the function is bijective, False otherwise.
        """
        # Check injectivity
        if len(set(self.mapping.values())) != len(self.mapping.values()):
            return False
        # Check surjectivity
        if set(self.mapping.values()) != self.target.space:
            return False
        return True

    def is_homeomorphism(self) -> bool:
        """
        Checks if the function is a homeomorphism.

        A **homeomorphism** is a bijective continuous function whose inverse is also continuous. Homeomorphisms preserve the topological structure between spaces, making them topologically equivalent.

        Returns:
        bool: True if the function is a homeomorphism, False otherwise.
        """
        if not self.is_bijective():
            print("The function is not bijective; therefore, it cannot be a homeomorphism.")
            return False

        # Create the inverse function
        inverse_mapping = {v: k for k, v in self.mapping.items()}
        try:
            inverse_function = Function(self.target, self.source, inverse_mapping)
        except ValueError as e:
            print(f"Could not create the inverse function: {e}")
            return False

        # Verify that the inverse function is continuous
        if not inverse_function.is_continuous():
            print("The inverse of the function is not continuous; therefore, it is not a homeomorphism.")
            return False

        # Verify that the function itself is continuous
        if not self.is_continuous():
            print("The function is not continuous; therefore, it is not a homeomorphism.")
            return False

        return True

    def __repr__(self) -> str:
        """
        Returns a string representation of the ContinuousFunction instance.

        Returns:
        str: String representation of the function.
        """
        return f"ContinuousFunction(\n  Mapping: {self.mapping}\n)"
