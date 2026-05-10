# ASA Projeto de Análise e Sintese de Algoritmos

2024/2025 project for the course of Analysis and Synthesis of Algorithms, containing 3 smaller sub-projects, each in their respective directory.

## First Sub-Project

### Problem Description
The first sub-project uses dynamic programming to apply parenthesis to an expression aiming to reach a target value, given the expression is composed of operations using a random operator defined as input.
For instance, if given the operator table:

<p align="center">
  <img width="207" height="182" alt="image" src="https://github.com/user-attachments/assets/419c1485-0fec-43de-8f29-3788a25fd61f" />  
</p>
  
And the expression:

$$
2⊕2⊕2⊕2⊕1⊕3 = 1
$$

Then the algorithm will dynamically find a solution by which the expression to the left is equal to the target value on the right. In this case, it would find:

$$
((((2⊕2)⊕2)⊕(2⊕1))⊕3) = 1
$$

### Solution Description
It achieves this result by first dividing the problem into subproblems, all of which start by placing parenthesis around a single expression, as such:

$$
a ⊕ b => (a ⊕ b)
$$

With this, the result matrix is built and, after all sub-problems are complete, returns the correct order of parenthesis, if one exists.

### Theoretical Analysis
**Complexity: $O(m^3 * n^2)$**, where $m$ is the row size of the operator matrix and n is the lenght of the expression. Most processing time is dedicated to filling the result matrix

## Second Sub-Project

### Problem Description
The Municipal Council of Caracolândia, influenced by the new trend of 15-minute cities, has decided to commission a study from Professor João Caracol in order to assess the efficiency of its urban transportation network. This study focuses on analyzing the line changes required to travel between any two stations in the metro network. The idea is to compute a metro connectivity index, *metro connectivity* `mc`, defined as follows:

$$mc = \max\{ML(e_1, e_2) \mid e_1, e_2 \in Metro\}$$

where $ML(e_1, e_2)$ denotes the minimum number of line changes required to travel between metro stations $e_1$ and $e_2$.

### Solution Description

From the input, we create two graphs:

- **`line_node_graph`**: the stations that make up each line
- **`node_line_graph`**: the lines that pass through each station

With these two graphs, we are able to build a graph that connects the lines to each other, which is much smaller and therefore much easier to examine with a BFS.

To optimize the code and handle some specific edge cases, we iterate through the list and remove any line that is a subset of another line in the graph (i.e., all the stations of one line are also stations of another). This produces an even smaller final graph with less redundancy.

### Theoretical Analysis

**Reading and writing the input data.** In this step we read the first line of input and the following `C` (connections) lines, placing the read data into the two graphs in constant time. The complexity of this step is `O(C)`.

**Removal of redundant lines.** Since it is possible to have lines completely contained within other lines — which are therefore irrelevant to the final result — this step removes such lines using two loops that iterate over the lines (`O(L^2)`), an `includes` operation with complexity `O(V)`, and a `for` loop to delete each element of the subset line, giving `O(L^2 * V^2)`.

**Applying the algorithm to compute the requested value.** The algorithm used for traversal is BFS, whose complexity is `O(V + C)`.

**Finding the largest connectivity index.** `O(L)`.

**Overall Complexity: $$O(L^2 \cdot V^2)$$**

## Third Sub-Problem
### Problem Description
Professor Natalino Caracol has been hired by Santa Claus's company, **UbiquityInc** in Rovaniemi, Lapland, to develop a program that produces the best possible distribution of Christmas toys to children around the world.

UbiquityInc follows a decentralized production strategy, with $n$ factories $F = \{f_1, \ldots, f_n\}$ distributed across $m$ countries $P = \{p_1, \ldots, p_m\}$ around the world. For production-optimization reasons, each factory $f_i$ produces a single type of toy and has a maximum stock of toys available for Christmas distribution, $f_{\max}^{i}$.

There are $t$ children $C = \{c_1, \ldots, c_t\}$ spread across the world who send letters to Santa Claus, with each child requesting a set of toys, of which they will receive at most one. For fairness reasons, UbiquityInc has established for each country $p_j$ a minimum number of gifts, $p_{\min}^{j}$, to be delivered in that country. Additionally, international trade rules limit the total exports from the set of all factories in each country $p_j$ to a maximum value of $p_{\max}^{j}$.

### Solution Description

**Decision variable:** $x_{k,i}$, which equals 1 when child $k$ receives a toy from factory $i$, and 0 otherwise.

**Objective function:**

$$\max \sum_{k=1}^{t} \sum_{i \in F_k} x_{k,i}$$

where $t$ is the total number of children, and $F_k$ is the set of factories that produce the gift child $k$ wants.

**Constraints:**

$$\sum_{i \in F_k} x_{k,i} \leq 1, \quad \forall k \in \{1, 2, \ldots, t\}$$

ensures that each child receives at most one gift.

$$\sum_{k \,:\, i \in F_k} x_{k,i} \leq f_{\max}, \quad \forall i \in \{1, 2, \ldots, n\}$$

ensures that factories do not exceed their maximum production.

$$\sum_{i \in P_j} \sum_{k \in C_{\sim j}} x_{k,i} \leq p_{\max}^{j}, \quad \forall j \in \{1, 2, \ldots, m\}$$

ensures that the maximum export limit of each country is not exceeded, where $P_j$ is the set of factories located in country $j$ and $C_{\sim j}$ is the set of children who are *not* in country $j$.

Finally,

$$\sum_{i \in P_j} \sum_{k \in C_j} x_{k,i} \geq p_{\min}^{j}, \quad \forall j \in \{1, 2, \ldots, m\}$$

where $C_j$ is the set of children who *are* in country $j$, ensures that the minimum domestic-distribution requirement of each country is met.

### Theoretical Analysis

The number of variables in the linear program is $O(|\text{children}| \times |\text{factories}|)$.

The number of variables in the linear program is $O(|\text{children}| \times |F|)$.

The number of constraints in the linear program is $O(|\text{children}| + |F| + 2 \times |P|)$:

- **Constraint 1** — each child receives at most one gift, so $O(t)$.
- **Constraint 2** — each factory has limited stock, so $O(n)$.
- **Constraints 3 and 4** — each country has a minimum of gifts received and a maximum of exports, so $O(2m) = O(m)$.

Given this, the complexity of the linear program is determined by the number of variables and constraints: $|F| \times |\text{children}|$ variables and $|F| + |\text{children}| + 2 \times |P|$ constraints.
