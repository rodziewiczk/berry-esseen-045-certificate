# Exact three-summand Berry--Esseen certificate

Research continuation, 6 September 2026.

## Mathematical result

For every real random variable X with E X = 0, E X^2 = 1 and
rho = E|X|^3 < infinity, and independent identically distributed copies,

    sup_x |P((X1+X2+X3)/sqrt(3) <= x) - Phi(x)| <= (59/250) rho.

Equivalently,

    C_3 <= 59 sqrt(3)/250 = 0.408763990586255... < C_E.

This is a computer-assisted proof, not the determination of the optimal C_3,
a literature-priority claim, a Lean-verified result, or a proof of the full
conjecture for every n. The analytic proof is in Three_summand_certificate.pdf.
The exact finite inequalities are in certificate/ and are recomputed by verify.py.

## Main new device

The seven one-coordinate features are

    (1, y, y^2-1, y^3, |y|^3, y^4, y^5).

We use 59 symmetric three-coordinate products: the 35 old low-feature products
and 24 additional products involving y^4 or y^5 and a zero-mean factor y or
y^2-1 in another coordinate. Independence makes those additional expectations
exactly zero. Thus the scalar expectation of the majorant still depends only
on gamma = E X^3 and rho; no unknown fourth or fifth moments are introduced.
Symmetrization is the AVERAGE over distinct permutations, not their sum.
The coefficient order is the lexicographic order of the allowed nondecreasing
index triples. Of the 59 features, 49 have zero expectation and 10 contribute
monomials in (gamma,rho).

An extremizer argument first proves that any violating globally maximizing law
has support in (-6,6). Higher moments are used only for this bounded witness.
The theorem itself assumes only a finite third absolute moment. The certificate
checks the larger cube [-7,7]^3 and the entire moment domain

    |gamma| <= 15/8,  1 <= rho <= 15/8,
    rho^2 (gamma^2 + 4) >= (gamma^2 + 2)^2.

The external probability input is Shevtsova's published structural bound
0.3322(1+0.429/rho). It handles rho >= 15/8 and supplies constants for the
contamination/support argument. The defect identity from the student note is
reproved in the supplement. No eventual-exactness theorem, local Fourier
certificate, effective N_0, two-point optimization, or previous C_2 bound is an
input to this C_3 proof.

## Reproduce

Required: Python 3, a C++17 compiler named g++, and Boost.Multiprecision headers.
The recorded run used CPython 3.13.5, g++ 14.2.0 and Boost 1.83 on Linux x86_64.
The acceptance path needs no NumPy, SciPy, SymPy, Arb, floating-point interval
library, or numerical Gaussian cdf implementation.

From this directory run:

    python verify.py

The script compiles check_cube.cpp afresh in a temporary directory. It reads
all rational certificate data, verifies exact consecutive coverage of
[-7/2,3/2], reconstructs the polynomials from the feature definition, checks
the whole support cube and moment domain, and checks the analytic constants.
A complete successful run ends with ACCEPTED_FULL_N3 and the scope/counts.
The exact output of the delivered run is in verification.log. It reports:

    ACCEPTED_FULL_N3 111 501156 219860 349

There are 111 intervals, 6,549 rational polynomial coefficients, 501,156 cube
nodes, 219,860 accepted cube leaves and 349 checked moment rectangles.

An additional standard-library exact audit is:

    python audit_initial_polynomials.py

It verifies all 95,904 tensor-grid identities for the original feature formula
and the initial Bernstein expansion. Since both expressions are degree at most
five in each coordinate, these checks prove polynomial identities on every
sign box. This is an independent calculation of the expansions, not a second
whole-proof implementation. Its output is in initial_identity_audit.log.

The optional symbolic identity cross-check requires SymPy:

    python verify_algebra.py

It is not a premise of the main acceptance path. The analytic proof, including
the variational and compactness arguments, remains a written mathematical proof;
the computer programs do not formally verify it.

## What the main checker proves

For each threshold interval [a,b], the 59 rational coefficients define M such
that, on all of [-7,7]^3,

    M(u,v,w) >= 1{u+v+w <= b}.

Its exact product-law expectation q(gamma,rho) satisfies throughout the whole
admissible moment domain

    q(gamma,rho) <= Phi(a/sqrt(3)) + (59/250)rho.

Sign orthants are treated separately. Symmetry only discards boxes with no
ordered triple; it never discards an admissible configuration. Polynomial
positivity is proved using tensor Bernstein coefficients and exact dyadic
subdivision. An affine Bernstein minorant handles the moving event plane.
All event-plane ties and all atoms are included. The normal cdf is enclosed
by alternating series, rational Machin bounds for pi, and integer square roots.

Malformed data, duplicate keys, noncanonical rational strings, gaps, overlaps,
unexpected files, symlinks, undecided positivity and resource-limit failures
cause rejection. The programs print success only after checking every cell.
Passing an individual cell is not a proof of the global theorem.

## Trust and construction boundary

The trusted project-specific surface is verify.py, check_cube.cpp, and the
analytic proof. Python integer/Fraction arithmetic, Boost's arbitrary-size
integers, the C++ compiler, OS and hardware are execution assumptions. No
floating-point arithmetic is used to decide acceptance. Construction involved
floating-point linear programming and floating-point separation, but construction
is not needed to reproduce verification and no construction score is trusted.

The C++ integer kernel and Python front end are complementary parts of one
verification implementation, not two implementation-diverse proofs. The earlier
C_2 independent checker was rerun successfully in this session; that result is
not an input to the present theorem. Independent mathematical and software
review, or a Lean port, would further strengthen confidence.

SHA256SUMS binds the proof, data, sources and logs. Hashes detect changes; they
are not a substitute for mathematical review or faithful execution.

## Remaining scope

The full Berry--Esseen conjecture remains unproved by this package. Combined
with the previous C_2 certificate and the one-summand bound used in the student's
note, the first not-yet-settled sample size in this programme is n=4. The same
feature principle yields 155 symmetric controls for four summands, still with
only gamma and rho as moment parameters. That observation is a research route,
not a four-summand certificate or a theorem for arbitrary n.
