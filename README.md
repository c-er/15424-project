<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

# Beyond *: Visualizing Quantifier Elimination for Real Arithmetic

This is the repository for my 15-424 term project, titled as above. Here are the current contents:
- `uni.sage` contains an implementation of univariate "Cohen-Hörmander" - so quoted because it skips
the sign matrix computation and replaces it with a black-box root finding algorithm from Sage. As
such, it only implements a part of the algorithm. To run, install [sagemath](https://www.sagemath.org/) and run `sage uni.sage`,
editing the formulae at the top of `uni.sage` as needed. Tested with `SageMath version 9.2`.
- `uni.js` is an incomplete implementation of the full univariate Cohen-Hörmander algorithm. All
the code from `uni.sage` has been ported, but it is not yet in a fit state to run. Depends on `Polynomial.js`
and `Fraction.js`, obtained from [here](https://github.com/infusion/Polynomial.js) and [here](https://github.com/infusion/Fraction.js)
respectively.
- `anim.py` is the code used to generate the animation `anim.mp4`. It uses the [manim library](https://github.com/3b1b/manim).
Installation instructions are located there; the animation can be generated via `manim anim.py`, passing
the `-l` switch for a more quickly generated, lower-quality animation.

Testing math: $$\exists x\, x^2 = 3$$

$$
\sum_{i = 1}^n i = \frac{n(n + 1)}{2}
$$

Testing GIF:

![](/animation/anim.gif)

