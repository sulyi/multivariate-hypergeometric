Generating Multivariate Hypergeometric Distribution
===================================================

Let's consider the following setup:
> * We take a set having _N_ number of elements.

> * We categorize these elements along some arbitrary requirement or requirements into _m_ number of categories.

> * We know there's exactly _n<sub>1</sub>,  n<sub>2</sub>, ..., n<sub>m</sub>_ elements in each category, therefore _&sum;n<sub>i</sub> = N, (i=1,2,...,m)_.

> * We choose a sample size of _K_ elements from the set above.

Where _N, K, m &in; &#x2115;<sub>0</sub>_ and _K &leq; N_.

Multivariate hypergeometric distribution describes the probabilities of cases of this situation. These cases can be identified by number of elements of each category in the sample, let's note them as follows by _k<sub>1</sub>, k<sub>2</sub>, ..., k<sub>m</sub>_, where _k<sub>i</sub> &leq; n<sub>i</sub>, (i=1, 2, ..., m)_.  
This is a generalisation of hypergeometric distribution, where _m = 2_.

Example:
--------

In a poker game there's _N = 52_ card in a deck and _m = 4_  suits each has _n<sub>i</sub> = 13_ ranks. Each player holds _K = 5_ cards. To calculate the probability of a flush we have to find the following cases _(k<sub>1</sub>,k<sub>2</sub>,k<sub>3</sub>,k<sub>4</sub>) = (5,0,0,0), (0,5,0,0), (0,0,5,0), (0,0,0,5)_.

Using the Classical Model
-------------------------

To calculate the probability of a case of this distribution we can use a calssic combinatoric formula:

> _P(k<sub>1</sub>,k<sub>2</sub>,...,k<sub>m</sub>) = **C**<sup>n<sub>1</sub></sup><sub style='position: relative; left: -1.1em;'>k<sub>1</sub></sub>&middot; **C**<sup>n<sub>2</sub></sup><sub style='position: relative; left: -1.1em;'>k<sub>2</sub></sub>&middot; ... &middot; **C**<sup>n<sub>m</sub></sup><sub style='position: relative; left: -1.3em;'>k<sub>m</sub></sub>/ **C**<sup>N</sup><sub style='position: relative; left: -.9em;'>K</sub>_.

Where _**C**<sup>n</sup><sub style='position: relative; left: -.6em;'>k</sub>_ is the binomial coefficient or _n_ over _k_.

Motivation
----------

Although this is a well known formula it's has the disadvantage being computationally demanding both in terms of CPU usage and representation of partial and final results. And even aside that this only gives us the probability of a single case, therfore we still need to find a solution to enumerate through each of them. Even if it isn't that difficult, there are some tricky parts, e.g. when _K > n<sub>i</sub>_.

Using the Law of Total Probability
----------------------------------

This project takes another approach and compaires it to the previous solution. Namely, it uses a lattice structure, where each level corespond to _K = 1, 2, ..., N_ distribution and calculates the probabilites using the formula of total probability. The examined algorithms enumerates the cases of these distributions in lexicographic order and exploit this to find indices of the conditional events in the adjasent distribution. It uses an implicit method to keep track of the ranking function. The lattice can be defined as _(&#x2115;<sup>m</sup>, MAX, MIN)_, where _MAX(A,B) = (max(a<sub>i</sub>,b<sub>i</sub>) | a<sub>i</sub> &in; A, b<sub>i</sub> &in; B, i=1,2,...,m)_ and _MIN_ is defined similarly.

Achievement and Tradeoff
----------------------

All in all this means that calaculateing a single probability can be done by _m_ division and same amount of multiplication, but in exchange of storing all of the probabilites of two distribution (one being calculated and, the adjesent one). Therefore this method is suitable for problems that need all these numbers anyway.

Final Thoughts
-------------

This is rather a proof of concept. Showcases the gain using such method to generate a multivariate distribution. There still should be plenty of chance to optimise this algorithm. And I'll continue to study this as time allows it.
