from .topology import Topology


class Function:
    """
    Represents a function between two topological spaces. It can be continuous, open, etc.

    Attributes:
    - source (Topology): The topological space from which the function originates.
    - target (Topology): The topological space to which the function maps.
    - mapping (dict): A dictionary mapping elements from the source space to the target space.
    """

    def __init__(self, source: Topology, target: Topology, mapping: dict):
        """
        Initializes a function between two topological spaces.
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
        """
        # For each open set in the target space, verify that the preimage is open in the source space
        for open_set in self.target.collection_of_subsets:
            preimage = self.get_preimage(open_set)
            if preimage not in self.source.collection_of_subsets:
                # Uncomment the print statement if you want to see which preimage is not open
                # print(f"The preimage of {sorted(open_set)} is {sorted(preimage)}, which is not open in the source space.")
                return False
        return True

    def is_open_mapping(self) -> bool:
        """
        Checks if the function is an open mapping.
        """
        # For each open set in the source space, verify that the image is open in the target space
        for open_set in self.source.collection_of_subsets:
            image = self.get_image(open_set)
            if image not in self.target.collection_of_subsets:
                # Uncomment the print statement if you want to see which image is not open
                # print(f"The image of {sorted(open_set)} is {sorted(image)}, which is not open in the target space.")
                return False
        return True

    def get_preimage(self, subset: set) -> set:
        """
        Obtains the preimage (inverse image) of a given set in the target space.
        """
        return {x for x in self.source.space if self.mapping.get(x) in subset}

    def get_image(self, subset: set) -> set:
        """
        Obtains the image of a given set in the source space.
        """
        return {self.mapping[x] for x in subset}

    def is_injective(self) -> bool:
        """
        Checks if the function is injective (one-to-one).
        """
        return len(set(self.mapping.values())) == len(self.mapping.values())

    def is_surjective(self) -> bool:
        """
        Checks if the function is surjective (onto).
        """
        return set(self.mapping.values()) == self.target.space

    def is_bijective(self) -> bool:
        """
        Checks if the function is bijective.
        """
        return self.is_injective() and self.is_surjective()

    def is_homeomorphism(self) -> bool:
        """
        Checks if the function is a homeomorphism.
        """
        if not self.is_bijective():
            return False

        # Create the inverse function
        inverse_mapping = {v: k for k, v in self.mapping.items()}
        try:
            inverse_function = Function(self.target, self.source, inverse_mapping)
        except ValueError as _:
            # Uncomment the print statement if you want to see why the inverse couldn't be created
            # print(f"Could not create the inverse function: {e}")
            return False

        # Verify that the inverse function is continuous
        if not inverse_function.is_continuous():
            return False

        # Verify that the function itself is continuous
        if not self.is_continuous():
            return False

        return True

    def __repr__(self) -> str:
        """
        Returns a string representation of the Function instance, including its properties.
        """
        # Basic representation
        mapping_str = ", ".join(f"{k} → {v}" for k, v in self.mapping.items())

        # Check properties
        properties = []

        if self.is_continuous():
            properties.append("Continuous")
        else:
            properties.append("Not Continuous")

        if self.is_open_mapping():
            properties.append("Open Mapping")
        else:
            properties.append("Not an Open Mapping")

        if self.is_bijective():
            properties.append("Bijective")
        else:
            injective = "Injective" if self.is_injective() else "Not Injective"
            surjective = "Surjective" if self.is_surjective() else "Not Surjective"
            properties.append(injective)
            properties.append(surjective)

        if self.is_homeomorphism():
            properties.append("Homeomorphism")
        else:
            properties.append("Not a Homeomorphism")

        # Build properties string
        properties_str = ', '.join(properties)

        return (f"Function(\n"
                f"  Source Topology: {self.source.collection_of_subsets}\n"
                f"  Target Topology: {self.target.collection_of_subsets}\n"
                f"  Mapping: {{ {mapping_str} }}\n"
                f"  Properties: {properties_str}\n)")
