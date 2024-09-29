# The Flying Tourist Problem

A tourist plans to visit several cities by plane and aims to spend as little
money as possible on flights.
- The trip must start and end in the tourist's home city.
- The tourist will stay a pre-defined number of nights in each city.
- The tourist will visit each city exactly once.
- The order in which the cities are visited is arbitrary.

# Modeling the Problem

From this description, we can extract three constraints:
1. The tourist cannot take a flight before their departure from home.
2. After arriving in a city, the tourist must depart exactly X days later.
3. The tourist will arrive in each city exactly once.

Condition 1 guarantees that the trip starts in the tourist's home city.

Condition 2 guarantees that the tourist's stay in each city, except for the home
city, adheres to the desired duration. It also guarantees that the trip ends at
the home city, as the tourist must eventually leave every stop.

Condition 3 guarantees that the tourist visits each city exactly once.

## Encoding

The solution to this problem can be modeled as a MaxSAT problem.

Let $V$ represent the set of cities the tourist will travel to, including their
home city. Let $base$ denote the city in $V$ corresponding to the tourist's home
city.

Variables used:
- For each flight, a variable $f_{o,a,d}$ that represents if a flight is to be
  taken, where $o$ is the city the flight departs from, $a$ the city in which it
  arrives, and $d$ it's date.

Hard clauses used:
- $(\neg f_{base,a_1,d_1} \wedge \neg f_{c,a_2,d_2})$, where
  $c \in V \setminus base$, and $d_2 < d_1$. This takes care of condition 1.
- $(\neg f_{o,c,d} \wedge f_{c,a_1,d + k_c} \wedge ... \wedge f_{c,a_n,d + k_c})$,
  where $c \in V \setminus base$. This takes care of condition 2.
- $\sum f_{o,c,d} = 1$, where $c \in V$. This takes care of condition 3.

Soft clauses used:
- $(f_{c,a,d})$, where $c \in V$ and with weight equal to
  $\dfrac{1}{Flight Cost}$. This is what guarantees we select the cheapest
  flight combination.
