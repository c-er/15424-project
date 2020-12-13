<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<script>
window.MathJax = {
  loader: {load: ['[tex]/color']},
  tex: {
    packages: {'[+]': ['color']},
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  }
};
</script>

$$
\newcommand{\R}{\mathbb{R}}
\newcommand{\N}{\mathbb{N}}
\newcommand{\Q}{\mathbb{Q}}
\newcommand{\inferrule}[3][]{\frac{#2}{#3}\,{#1}}
$$

# Beyond $\ast$: Visualizing Quantifier Elimination for Real Arithmetic

<p align="center">
<img src="logo.png">
</p>

**Abstract**: The existence of a quantifier elimination algorithm for real arithmetic is one of the foundational results that enables formal reasoning and verification of CPS. Most of the well-known algorithms for quantifier elimination are extremely complicated, too inefficient to be used on even the simplest of formulae, or both. This makes studying quantifier elimination algorithms difficult. This project aims to rectify this problem by providing a writeup and implementation of the Cohen-Hörmander algorithm along with some visualizations to aid understanding.

# Introduction

The modeling of cyber-physical systems (CPS), and the subsequent formal verification of the model, are made possible by a multitude of results. Foremost
among these is the development of a logic (such as differential dynamic logic) that can express desirable properties of a CPS as logical formulae, along
with a set of inference rules that can be used to construct proofs of these formulae. Manually constructing these computationally-verifiable proofs from the axioms
of all the formal logics involved would be far too painful even for simple CPS. It thus becomes important to seek methods of automating the proof construction.

While it is impossible for many useful logics to fully automate the proof construction process (CITE HERE), it is certainly possible to automate portions
of it. Rather surprisingly, a 1931 result by Tarski (CITE HERE), along with related more recent developments (CITE HERE), show that the entire proof construction
process can be automated once the desired goal has been reduced to proving a formula of real arithmetic. This result is absolutely foundational for CPS verification, both
from a theoretical and a practical perspective. The existence of an automatic verification procedure for formulae of real arithmetic allows one to abstract away the formal reasoning
process behind the real arithmetic proof goals, and simply give inference rules such as the following, which holds whenever $\bigwedge \Gamma \implies \bigvee \Delta$ is a valid
formula of real arithmetic (CITE HERE).

$$
\inferrule{\ast}{\,\,\Gamma \vdash \Delta\,\,}{\color{blue}{\R}}
$$

Practically speaking, the real arithmetic proof goals that result from attempts to prove properties of CPS are often prohibitively complex for manual methods.

Given the significance of this result, and the rather mysterious nature of the real arithmetic proof rule, the question "what is really going on here?" likely crosses many students' minds.
A little research would reveal a number of algorithms for automatically deciding the truth of a sentence of real arithmetic (called quantifier elimination (QE) algorithms), but many of the choices have significant disadvantages:

- **Tarski's original algorithm** was a very important theoretical breakthrough, but complicated and so inefficient that it isn't useful for anything besides theoretical purposes (CITE HANDBOOK). Given the complexity of this algorithm, understanding it would be difficult, and given the inefficiency, interaction with an implementation (which would be very useful for understanding) would not be feasible.
- **Cylindrical-Algebraic Decomposition (CAD)** is the state of the art when it comes to practical QE, so it doesn't suffer from the inefficiency problem of Tarski's algorithm (CITE HERE). However, it is incredibly complicated: so much so that it took experts in the field 30 years to produce a working implementation (CITE HERE). As such, it is likely not suitable for a student in an introductory CPS class.
- **Virtual substitution** is efficient (CITE HERE), and simple enough to be part of CMU's introductory 15-424 _Logical Foundations of Cyber-Physical Systems_ course. The only shortcoming of this algorithm is that it isn't complete, in the sense that there are theoretical limitations that prevent it from deciding the truth of arbitrary sentences of real arithmetic (CITE HERE). Understanding this algorithm is thus not equivalent to understanding what's going on behind the scenes of the $\R$ proof rule.

However, there is a (not too well-known) alternative that offers a reasonable balance: the **Cohen-Hörmander** algorithm (CITE ORIG HERE). It is simple enough to be described in full in this paper, complete in the sense that it can (in principle) decide the truth of any sentence of real arithmetic, and efficient enough to admit implementations that one can actually interact with. This work thus aims to introduce an audience of students taking introductory logic courses to real quantifier-elimination by providing a writeup, a number of visuals, and an interactive implementation of the Cohen-Hörmander algorithm.

## Related Work

Mention the CAD visualization guy.

# Background

In this section, we very briefly review some of the background material that is necessary to properly
define the problem solved by the Cohen-Hörmander algorithm. 

## Real Arithmetic

The first-order theory of real closed fields is a
formal language for stating properties of the real numbers. The language is built up recursively as
follows:

**Terms**: Terms are the construct that the language uses to refer to real numbers, or to combine existing
numbers into other ones. They are built up via the following inference rules

$$
\inferrule{c \in \Q}{c\,\mathsf{term}}{} \qquad
\inferrule{x\,\mathsf{var}}{x\,\mathsf{term}}{} \qquad
\inferrule{e_1\,\mathsf{term}\quad e_2\,\mathsf{term}}{e_1 + e_2\,\mathsf{term}}{} \qquad
\inferrule{e_1\,\mathsf{term}\quad e_2\,\mathsf{term}}{e_1 \cdot e_2\,\mathsf{term}}{}
$$

**Formulae:** Formulae are the construct that the language uses to express assertions about
real numbers. The basic, or atomic, formulae are constructed as follows:

$$
\inferrule{e_1\,\mathsf{term}\quad e_2\,\mathsf{term}}{e_1 = e_2\,\mathsf{form}}{} \qquad
\inferrule{e_1\,\mathsf{term}\quad e_2\,\mathsf{term}}{e_1 < e_2\,\mathsf{form}}{} \qquad
\inferrule{e_1\,\mathsf{term}\quad e_2\,\mathsf{term}}{e_1 > e_2\,\mathsf{form}}{} \qquad
\inferrule{e_1\,\mathsf{term}\quad e_2\,\mathsf{term}}{e_1 \leq e_2\,\mathsf{form}}{} \qquad
\inferrule{e_1\,\mathsf{term}\quad e_2\,\mathsf{term}}{e_1 \geq e_2\,\mathsf{form}}{} \qquad
$$

Formulae can be joined together using boolean connectives:

$$
\inferrule{\varphi\,\mathsf{form}}{\neg\varphi\,\mathsf{form}}{} \qquad
\inferrule{\varphi\,\mathsf{form}\quad \psi\,\mathsf{form}}{\varphi \wedge \psi\, \mathsf{form}}{} \qquad 
\inferrule{\varphi\,\mathsf{form}\quad \psi\,\mathsf{form}}{\varphi \vee \psi\, \mathsf{form}}{} \qquad
\inferrule{\varphi\,\mathsf{form}\quad \psi\,\mathsf{form}}{\varphi \implies \psi\, \mathsf{form}}{} \qquad
\inferrule{\varphi\,\mathsf{form}\quad \psi\,\mathsf{form}}{\varphi \iff \psi\, \mathsf{form}}{}
$$

Finally, variables occuring in terms can be given meaning by way of quantifiers.

$$
\inferrule{\varphi\,\mathsf{form}\quad x\,\mathsf{var}}{\forall x\, \varphi\,\mathsf{form}}{} \qquad
\inferrule{\varphi\,\mathsf{form}\quad x\,\mathsf{var}}{\exists x\, \varphi\,\mathsf{form}}{} \qquad
$$

Real arithmetic is what we get when we give these syntactic constructs their natural meaning over
the real numbers. That is, the symbols $+, \cdot, =, <$, etc denote addition, multiplication, equality,
and comparison of real numbers respectively. Quantifiers are interpreted to range over the real numbers.

With these constructs, we can formally express many properties of the real numbers.
Some examples include:
- Every number is positive, negative, or zero: $\forall x\, (x > 0 \vee x < 0 \vee x = 0)$.
- Every number has an additive inverse: $\forall x\, \exists y\, (x + y = 0)$.
- Every nonzero number has a multiplicative inverse: $\forall x\, (x = 0 \vee \exists y\, (x \cdot y = 1))$.

However, not everything that we intuitively think of as a property of the real numbers can actually be
accurately expressed in this language. A typical example is the supremum property: the assertion that
every nonempty set of real numbers which is bounded above has a least upper bound has no equivalent
in this language (CITE HERE). As we shall shortly see, the expressiveness (or lack thereof) of this language
is key to the operation of the Cohen-Hörmander algorithm.

Now we can properly define what the Cohen-Hörmander algorithm actually does. It is a quantifier-elimination
algorithm: it takes as input a formula $\varphi$ in this language, and produces a formula $\psi$ which
contains no quantifiers and whose free variables are a subset of the free variables of $\varphi$.
Moreover, $\psi$ and $\varphi$ have the same truth value regardless of how we choose to substitute for
the real variables.
- $\exists y\, (x < y \wedge y \leq 0)$ might be reduced to $x < 0$, because regardless of which value in $\R$
we choose to assign to $x$, the two formulaes are either both true or both false.
- $\forall x\, (x > 0 \vee x < 0 \vee x = 0)$ might be reduced to $\top$, the formula which is always
true. Indeed, since the original formula has no free variables, the quantifier-eliminated formula
also cannot have free variables, and thus must be equivalent to either $\top$ (true) or $\bot$ (false).

## Real Analysis/Algebra

In this section, we list a few definitions and theorems of basic analysis/algebra that are useful in understanding
the Cohen-Hörmander algorithm. 

**Definition** (Sign):The sign of a real number $x$ is
- $+$, or positive, when $x > 0$
- $0$ when $x = 0$
- $-$, or negative, when $x < 0$

**Theorem** (Intermediate value): If $f$ is a continuous function of $x$ (in particular, if $f$ is a polynomial in $x$),
$a < b$, and the signs of $f(a)$ and $f(b)$ do not match, then $f$ has a root in $[a, b]$.

**Definition** (Polynomials with rational coefficients): $\Q[x]$ denotes the set of all polynomials in $x$
with coefficients in $\Q$.

**Theorem** (Polynomial division): If $a, b \in \Q[x]$ and $b \neq 0$, there exists unique
$q, r \in \Q[x]$ satisfying
- $a = bq + r$
- $\mathrm{deg}(r) < \mathrm{deg}(b)$.

# The Algorithm

Our approach will be to first treat the simpler univariate case: formulas of the form $\forall x\, \varphi$ or $\exists x\, \varphi$
such that the only variable in $\varphi$ is $x$. Then we will discuss how to generalize to the general case.

## Univariate Case

A priori, deciding the truth of a formula of the form $\forall x\, \varphi$ or $\exists x\, \varphi$ requires looping
through every single $x \in \R$, substituting that value into $\varphi$, checking the result, and then
combining the results for all $x \in \R$ in the manner that suits the quantifier. This approach works
when the model we're concerned with is finite, but since $\R$ is very much not finite, this cannot
possibly yield a useful algorithm. 

### Understanding the Sign Matrix

The first step in unlocking a decision procedure for real arithmetic is to look closely at what formulae
in this language can express. All formulae are ultimately built up from atomic formulae, and atomic formulae
are built out of terms, so we'll start there.

Recall the inductive construction of terms: we started with rational constants
and variables (in our present case, only $x$), and we were allowed to combine terms into larger terms
by adding and multiplying. Using multiplication only, starting with rational constants and $x$, we'll
get terms of the form $qx^n$, where $q \in \Q$ and $n \in \N$. These are **monomials** (with rational coefficients) in $x$.
Add addition into the mix, and since multiplication distributes over addition, we arrive at our first important observation:
**a term is a polynomial in $x$ with rational coefficients.**

Atomic formula were constructed as $e_1 \textsf{ CMP } e_2$, where $e_1, e_2$ are terms and $\mathsf{CMP}$
was one of $=$, $<$, $>$, $\leq$, or $\geq$. Since terms are polynomials in $x$, atomic formulae are
comparisons between polynomials. But $e_1 \textsf{ CMP } e_2$ is equivalent to $e_1 + (-1) \cdot e_2 \textsf{ CMP } 0$
for any choice of $\mathsf{CMP}$, and $e_1 + (-1) \cdot e_2$ is also a term, and therefore a polynomial.
Thus, **every atomic formula asserts something about the sign of a polynomial.** For example, the atomic formula $3x^2 + 2 \geq 2x + 1$
equivalently asserts that the polynomial $3x^2 - 2x + 1$ is positive or zero.

This realization is key to transforming our infinite loop over $\R$ that we had in our initially proposed
algorithm into a finite loop. Polynomials (with the zero polynomial being an easy special case) have only
finitely many roots. Between two consecutive roots (also before the first root, and after the last root),
a polynomial must maintain the same sign, since
if it changed sign, by the intermediate value theorem there would have to be another root in the middle.
The upshot is that if $x_1, \dots, x_n$ are the roots of a polynomial $p$ in increasing order, then by knowing the sign of $p$
at one point in each of the intervals $(-\infty, x_1), (x_1, x_2), \dots, (x_{n - 1}, x_n), (x_n, \infty)$,
we know the sign of $p$ for every $x \in \R$. Since the truth of an atomic formula $p \textsf{ CMP } 0$ at a point $x$
is a function of the sign of $p$ at $x$, **given a finite data structure which specifies the signs of $p$ over the intervals $(-\infty, x_1), (x_1, x_2), \dots, (x_{n - 1}, x_n), (x_n, \infty)$, we can evaluate an atomic formula at any $x \in \R$.** Note that the signs at the points $x_1, \dots, x_n$ are all $0$,
since $x_1, \dots, x_n$ are the roots of $p$, so in the case where we're dealing with just a single polynomial,
we don't need to include the sign information at the roots in the data structure.

A quantifier-free formula $\varphi$ is just a propositional combination of a bunch of atomic formulae,
and as such, knowing the truth value of each of the composite atomic formulae is sufficient to determine
the truth value of $\varphi$. Above we discussed how to obtain a finite data structure that gives us
the truth value of an atomic formulae at any $x \in \R$ - so all we need to do is combine these data
structures for all the (finitely many) atomic formulae that are in $\varphi$, and we obtain a finite
data structure which can be used to evaluate $\varphi$ at any point $x$. This is exaftly the **sign matrix**
data structure which is the core of the Cohen-Hörmander algorithm.

More formally, the rows of the sign matrix are indexed by the polynomials in $S_\varphi$. If $x_1, \dots, x_n$ are an exhaustive list of all the roots of the polynomials in $S_\varphi$ with $x_1 < x_2 < \cdots < x_n$, then the columns of the sign matrix are indexed by the list

$$(-\infty, x_1), x_1, (x_1, x_2), x_2, \dots, (x_{n - 1}, x_n), x_n, (x_n, \infty)$$

i.e, the singleton sets at the roots and the intervals between them. The entry of the sign matrix at row $p \in S_\varphi$
and column $I$ is just the sign of $p$ on $I$. Just as before, note that the signs of all the polynomials are invariant on each interval, because
if a polynomial (or any continuous function, for that matter) changes sign on an interval, it must have a root in that interval.
But since $x_1, \dots, x_n$ is a list of ALL of the roots of the polynomials in $S_\varphi$, and no interval listed above
contains any of these points, this is not possible. Note also that in this case, where we potentially have multiple
polynomials, we do need to specify the sign of each polynomial at each root: the presence of $x_i$ as a column only
means that $x_i$ is a root of one of the polynomials involved - the other polynomials may have nonzero sign at $x_i$.

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
<img src="animation/gif/signmat_meaning.gif">
</p>

Finally, here's an animation that shows how this sign matrix can be used to compute the truth value
of the formula $\forall x\, [(p_1(x) \geq 0 \wedge p_2(x) \geq 0) \vee (p_3(x) > 0)]$. Note how
the fact that the signs of the polynomials (and thus the truth values of the atomic formulae) are invariant
over each column of the sign matrix allows us to effectively iterate over all of $\R$ by only checking
each column of the sign matrix.

<p align="center">
<img src="animation/gif/signmat_usage.gif">
</p>

One important thing to note is that while the sign matrix relies crucially on the ordering of the
roots of the polynomials involved, it doesn't actually contain any numerical information about the
roots themselves. In our toy example, it's easy to see that $x_1 = -1$ and $x_2 = 1$, but this isn't
recorded in the sign matrix, nor is it necessary for the final decision procedure.

### Computing the Sign Matrix

Unfortunately, building the sign matrix for an arbitrary set of polynomials isn't as simple as telling
the computer to "draw a graph," as we did in the animation above.

# Conclusion

# Deliverables

# References

Pandoc