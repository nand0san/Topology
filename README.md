# Finite Topology Library

A Python library for defining, analyzing, and exploring **finite topologies**. This toolset is designed for educational purposes, to assist in research, and to make it easy to experiment with topological concepts computationally, using **finite sets**. 

## Features

- **Construct Common Topologies**: 
  - **Discrete Topology**: Every subset is open.
  - **Indiscrete (Trivial) Topology**: Only the empty set and the entire set are open.
  - **Sierpiński Topology**: A classic topology on a two-element set.
  - **Particular Point and Excluded Point Topologies**: Control which points are required or excluded in open sets.
  - **Divisibility Topology**: Topology based on divisibility relations among integers.
  - **Alexandrov Topology**: Topologies that are closed under arbitrary intersections of open sets, useful in domain theory.
  
- **Analyze Functions Between Spaces**:
  - **Continuity**: Check whether a function between two topological spaces is continuous.
  - **Homeomorphism**: Analyze whether two spaces are homeomorphic (topologically equivalent) via bijections.
  - **Preimage and Image**: Compute preimages of sets under continuous mappings.
  
- **Topology Properties**:
  - **Compactness**: Determine if a topology is compact, a trivial property for finite topologies.
  - **Connectedness**: Check if the space can be split into two disjoint open sets.
  - **Hausdorff Conditions (T2)**: Verify if any two distinct points have disjoint open neighborhoods.
  - **Separation Axioms (T0, T1)**: Study basic separation properties in finite spaces.

## Installation

To install the library, run the following command:

```bash
pip install finite-topology
```

Alternatively, you can clone the repository and install dependencies:

```bash
git clone https://github.com/nand0san/Topology.git
cd finite-topology
pip install -r requirements.txt
```

## Usage

### Example 1: Create a Discrete Topology and Analyze a Continuous Function

```python
from finite_topology.known_topologies import create_discrete_topology
from finite_topology.functions import Function

# Define two sets
space = {1, 2, 3}
target_space = {'a', 'b', 'c'}

# Create discrete topologies on both spaces
source_topology = create_discrete_topology(space)
target_topology = create_discrete_topology(target_space)

# Define a mapping for a continuous function
mapping = {1: 'a', 2: 'b', 3: 'c'}

# Create a function and verify continuity
f = Function(source_topology, target_topology, mapping)
print(f"Is the function continuous? {f.is_continuous()}")
```

### Example 2: Study Dense Sets in Finite Topologies

In finite topologies, dense sets have interesting behavior. Consider the triviality of the entire space being dense in many cases.

```python
from finite_topology.topology import Topology

# Create a topology
space = {1, 2, 3}
subsets = [{1}, {1, 2}, space]
topology = Topology(space, subsets)

# Find the dense subsets
dense_set = topology.find_dense_subset()
print(f"Dense subset: {dense_set}")
```

**Explanation**: In finite topologies, if the closure of a subset equals the entire space, the subset is dense. The library can compute and return the smallest dense subset or indicate if the entire space is the only dense subset.

### Example 3: Topologies with Specific Points (Particular Point Topology)

```python
from finite_topology.known_topologies import create_particular_point_topology

space = {1, 2, 3}
particular_point = 2

# Create a particular point topology
topology = create_particular_point_topology(space, particular_point)

print(f"Topology with particular point {particular_point}:")
print(topology)
```

In this example, the topology is defined such that every non-empty open set must contain the particular point.

### Example 4: Checking Hausdorff Conditions (T2)

```python
from finite_topology.known_topologies import create_trivial_topology

# Create a trivial topology
space = {1, 2, 3}
topology = create_trivial_topology(space)

# Check if the topology is Hausdorff
print(f"Is the topology Hausdorff? {topology.is_hausdorff()}")
```

**Note**: In finite spaces, the only Hausdorff topology is the discrete topology, as shown in [this Math StackExchange discussion](https://math.stackexchange.com/questions/1567152/a-finite-hausdorff-space-is-discrete).

## More Advanced Usage

For a more in-depth exploration, the **Jupyter notebooks** in the [GitHub repository](https://github.com/nand0san/Topology/tree/main) offer guided examples on topics like:

- Constructing topologies based on **equivalence relations**.
- Exploring the interaction between topologies and **continuous functions**.
- Understanding the behavior of **dense sets** in topological spaces.
- Visualizing **basis** for topologies and how they define open sets.

## Documentation

The complete documentation, including class details and function usage, is generated via Sphinx and hosted on [GitHub Pages](https://nand0san.github.io/Topology/_build/html/index.html).

## Contributing

Feel free to contribute! Open an issue or submit a pull request for improvements, bug fixes, or new features.