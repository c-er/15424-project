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

The first important observation that underlies the Cohen-H\"ormander algorithm is that sentences of the form $\forall x\, \varphi$ or $\exists x\, \varphi$ are essentially assertions about the signs ($0$, positive, or negative) of polynomials. We build up to this realization from the following simple facts:
- Terms of first-order real arithmetic are polynomials in $x$.
- Atomic formulae in real arithmetic are equalities or inequalities between terms.
- Since terms are polynomials, this means that every atomic formula is of the form $p_1 \textsf{ CMP } p_2$, where $\textsf{CMP}$ is one of: $=$, $<$, $>$, $\leq$, $\geq$.
- The formula $p_1 \textsf{ CMP } p_2$ is equivalent to $p_1 - p_2 \textsf{ CMP } 0$ for any choice of $\textsf{CMP}$.
- $p_1 - p_2$ is also a polynomial, and therefore $p_1 - p_2 \textsf{ CMP } 0$ expresses something about the sign of a polynomial.

Does displaymath still work?

$$\sum_{i = 1}^n i = \frac{n(n + 1)}{2}$$

$$
\sum_{i = 1}^n i = \frac{n(n + 1)}{2}
$$

well does it
$$\sum_{i = 1}^n i = \frac{n(n + 1)}{2}$$

Gif:

![](/animation/signmat_meaning.gif)

