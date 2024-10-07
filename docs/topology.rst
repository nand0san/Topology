Topology
========

**Formal Definition**

A **topology** on a set \\(X\\) is a collection \\(\\tau\\) of subsets of \\(X\\) such that:

- The empty set and \\(X\\) itself are in \\(\\tau\\).
- \\(\\tau\\) is closed under arbitrary unions.
- \\(\\tau\\) is closed under finite intersections.

.. math::

    \text{A topology } \tau \text{ on a set } X \text{ satisfies:} \\
    \emptyset, X \in \tau, \\
    \forall \{ U_i \}_{i \in I} \subseteq \tau, \quad \bigcup_{i \in I} U_i \in \tau, \\
    \forall U_1, U_2, \dots, U_n \in \tau, \quad \bigcap_{j=1}^n U_j \in \tau

This class allows working with finite topological spaces, defined by providing a space and a collection of subsets.

.. automodule:: topology
   :members:
   :undoc-members:
   :show-inheritance:
