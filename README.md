<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<script>
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  }
};
</script>

# Beyond *: Visualizing Quantifier Elimination for Real Arithmetic

The first important observation that underlies the Cohen-Hörmander algorithm is that sentences of the form $\forall x\, \varphi$ or $\exists x\, \varphi$ are essentially assertions about the signs ($0$, positive, or negative) of polynomials. We build up to this realization from the following simple facts:
- Terms of first-order real arithmetic are polynomials in $x$.
- Atomic formulae in real arithmetic are equalities or inequalities between terms.
- Since terms are polynomials, this means that every atomic formula is of the form $p_1 \textsf{ CMP } p_2$, where $\textsf{CMP}$ is one of: $=$, $<$, $>$, $\leq$, $\geq$.
- The formula $p_1 \textsf{ CMP } p_2$ is equivalent to $p_1 - p_2 \textsf{ CMP } 0$ for any choice of $\textsf{CMP}$.
- $p_1 - p_2$ is also a polynomial, and therefore $p_1 - p_2 \textsf{ CMP } 0$ expresses something about the sign of a polynomial.

The quantifier-free formula $\varphi$ is thus (equivalent to) a propositional combination of a bunch of assertions about the signs of some finite set $S_\varphi$ of polynomials. In other words, if we know the signs of all the polynomials in $S_\varphi$ at some point $x$, we can decide whether $\varphi$ is true or false at $x$. Now, how often do the signs of the polynomials in $S_\varphi$ change? Only finitely often - any given polynomial can only potentially change sign at its roots. Polynomials (with the zero polynomial being an easy edge case) have only finitely many roots, and $S_\varphi$ is a finite set of polynomials. Therefore, if we can obtain information about the signs of the polynomials in $S_\varphi$ at each of the roots of the polynomials and the intervals between the roots, we effectively capture the signs of all the polynomials in $S_\varphi$ at every $x \in \mathbb{R}$ in a finite data structure. This is exactly the **sign matrix** data structure computed in the Cohen-Hörmander algorithm.

More formally, the rows of the sign matrix are indexed by the polynomials in $S_\varphi$. If $x_1, \dots, x_n$ are an exhaustive list of all the roots of the polynomials in $S_\varphi$ with $x_1 < x_2 < \cdots < x_n$, then the other dimension of the sign matrix is indexed by 

$$(-\infty, x_1), x_1, (x_1, x_2), x_2, \dots, (x_{n - 1}, x_n), x_n, (x_n, \infty)$$

i.e, the singleton sets at the roots and the intervals between them. The entry of the sign matrix at column $p \in S_\varphi$
and row $I$ is just the sign of $p$ on $I$. Note that the signs of all the polynomials are invariant on each interval, because
if a polynomial (or any continuous function, for that matter) changes sign on an interval, it must have a root in that interval.
But since $x_1, \dots, x_n$ is a list of ALL of the roots of the polynomials in $S_\varphi$, and no interval listed above
contains any of these points, this is not possible.

Here's an example of a sign matrix for the set of polynomials $\{p_1, p_2, p_3\}$,
where $p_1(x) = 4x^2 - 4$, $p_2(x) = (x + 1)^3$, and $p_3(x) = -5x + 5$.

$$
\begin{array}{cccccc}
    & (-\infty, x_1) & x_1 & (x_1, x_2) & x_2 & (x_2, \infty) \\
p_1 & + & 0 & - & 0 & + \\
p_2 & - & 0 & + & + & + \\
p_3 & + & + & + & 0 & -
\end{array}
$$

And here's an animation that illustrates the meaning of the sign matrix.

<p align="center">
<img src="/animation/signmat_meaning.gif">
</p>

![](/animation/signmat_meaning.gif)

