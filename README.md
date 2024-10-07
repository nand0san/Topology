

# Finite Topology Helper Library

A Python library for creating and working with different types of topologies on finite sets. This library provides utility functions to define various topological structures and to manipulate continuous mappings between them. It is intended for educational purposes and for researchers who wish to explore basic topological concepts in a computational manner.

## Features
- **Create Common Topologies**: Functions to create well-known topologies such as:
  - **Discrete Topology**: Every subset is open.
  - **Trivial (Indiscrete) Topology**: Only the empty set and the entire space are open.
  - **Sierpiński Topology**: A basic topology on a two-element set.
  - **Particular Point and Excluded Point Topologies**: Customize which elements are necessarily included or excluded in open sets.
  - **Divisibility and Upward Closed Topologies**: Specialized topologies useful in algebra and order theory.
  - **Topology from Equivalence Relations**: Construct topologies from equivalence relations and partial orders, including Alexandrov topologies.
- **Study Functions Between Topologies**: Define continuous functions, check for continuity, bijectivity, and homeomorphisms. Create and verify properties of continuous mappings in different finite topological spaces.
- **Topology Analysis**: Explore properties such as compactness, connectedness, and Hausdorff conditions for different finite topologies.
- **Interactive Notebooks for Learning**: Step-by-step Jupyter notebooks that guide users through examples of topology creation, function mapping, and analysis, enriched with detailed explanations and visualizations.

## Installation
To use this library, install it from PyPI:

```sh
pip install finite-topology
```

Alternatively, you can clone the repository and install the required dependencies:

```sh
git clone https://github.com/nand0san/Topology.git
cd finite-topology
pip install -r requirements.txt
```
## Github

The project is public domain and can be found in the repository: 

https://github.com/nand0san/Topology.git

## Usage

Here is a simple example demonstrating how to create a discrete topology and a continuous function between two topological spaces:

```python
from finite_topology.known_topologies import create_discrete_topology
from finite_topology.functions import ContinuousFunction

# Define the space
space = {1, 2, 3}

# Create a discrete topology on the space
discrete_topology = create_discrete_topology(space)

# Define a mapping for a continuous function
mapping = {1: 'a', 2: 'b', 3: 'c'}

# Create target topology
target_space = {'a', 'b', 'c'}
target_topology = create_discrete_topology(target_space)

# Create the continuous function
function = ContinuousFunction(discrete_topology, target_topology, mapping)
print("Is the function continuous?", function.is_continuous())
```

## Modules Overview

- **topology.py**: Defines the `Topology` class and methods to operate on topological structures, including checks for various properties (e.g., compactness, connectedness, Hausdorff conditions).
- **functions.py**: Defines continuous functions between topological spaces and provides tools to study their properties (e.g., continuity, bijectivity, homeomorphisms).
- **helpers.py**: Contains various utility functions to create specific topologies, like discrete, trivial, Sierpiński, etc.
- **interactive_notebooks**: A collection of Jupyter notebooks that illustrate the use of the library, allowing users to experiment with topological concepts interactively.

## Documentation
Detailed documentation for each function and class can be found in the `docs/` folder. You can generate the HTML version of the documentation by running:

```sh
cd docs
make html
```

Also, existing jupyter notebooks with examples and details in github.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you'd like to contribute code or documentation improvements.

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.

## Contact
For any questions, feel free to contact [nand0san](https://github.com/nand0san) via GitHub.