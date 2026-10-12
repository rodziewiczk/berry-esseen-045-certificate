# Physical quadrature for a first critical fourth index

A hypothetical fourth-index extremizer has bounded support. This gives
the fourth moment needed to control the entire Prawitz quadrature directly.
Consequently a rigorous bound on its finite midpoint polynomial needs only
one physical quadrature reserve. Separate quadrature estimates for the
signed transfer, the optimized error radius, and the nonlinear remainder
are unnecessary. This is a conditional reduction for excluding an attained
critical extremizer, not a bound for every unbounded standardized law.

## Hypotheses and proof boundary

Assume the retained all-law result \(C_3<C_E\). Let \((P,H)\) be an attained,
positively oriented closed maximum with \(C_4\ge C_E\), where
\(EX=0\), \(EX^2=1\), \(\rho=E|X|^3\). The existing
[first critical radius proof](first_critical_support_17_4_2026_10_01.md)
gives
\[
 \operatorname{supp}P\subset(-17/4,17/4),\qquad \rho<46/25.
 \tag{1}
\]
Its analytic inputs are critical-level attainment, the finite contact
identity and Gaussian estimate of He–Cheng, and Shevtsova's finite iid
envelope. The one-sided closed-CDF Prawitz theorem is a further explicit
input below. No new fourth-moment assumption is introduced.

The statement \(C_3\le59\sqrt3/250<C_E\) is retained in the manuscript;
the strict elementary comparison is
\[
 (256/625)^2-(59\sqrt3/250)^2=1069/1562500>0.
\]
This note does not replace that computer-assisted proof or its analytic
inputs by a new Lean verification.

## Moments of the physical fourfold sum

Set \(Z=(X_1+X_2+X_3+X_4)/2\), with independent copies of \(X\). From (1),
\[
 EX^4\le(17/4)\rho<391/50<8,
\]
and independence and centering give
\[
 EZ=0,\quad EZ^2=1,\quad EZ^3=EX^3/2,\quad
 EZ^4=(EX^4+9)/4<17/4.
\]
In particular \(|EZ^3|\le\rho/2<23/25<6/5\). For \(|x|\le2\), put
\(D=x-Z\). Then
\[
 ED^2=x^2+1\le5,
\]
\[
 ED^4=x^4+6x^2-4xEZ^3+EZ^4
 <16+24+48/5+17/4=1077/20<54.
\]
Cauchy therefore gives
\[
 E|D|<9/4,\qquad
 E|D|^3\le\sqrt{ED^2ED^4}<33/2.
 \tag{2}
\]
These are bounds for the original physical law, not merely its finite
Q3 reference. No restriction on the number of support points is used.

## Regular Prawitz integrand

For \(0<u<1\), write
\[
 R(u)=(1-u)\cot(\pi u)+1/\pi,\qquad S(u)=uR(u).
\]
The retained partial-fraction calculation proves, on the closed interval,
\[
 0\le S\le1/3,\qquad |S'|<2,\qquad |S''|<5.
 \tag{3}
\]
For \(\lambda=6D\), set
\[
 A(u)=E\cos(\lambda u),\qquad
 L(u)=E[\lambda\operatorname{sinc}(\lambda u)].
\]
The closed-CDF Prawitz majorant is
\[
 P(Z\le x)\le J_P(x)=\frac12+\int_0^1 F_x(u)\,du,
 \qquad F_x(u)=(1-u)A(u)+S(u)L(u).
 \tag{4}
\]
The apparent \(1/u\) singularity has been removed before differentiation.
Using \(\operatorname{sinc}(v)=\int_0^1\cos(tv)\,dt\), (2) yields
\[
 |A'|<27/2,\quad |A''|\le180,
 \qquad |L|<27/2,\quad |L'|\le90,\quad |L''|<1188.
\]
Differentiation under the expectation is justified by the displayed first,
second, and third absolute moment bounds. Thus
\[
 |((1-u)A)''|<207,
\]
\[
 |(SL)''|<5(27/2)+4(90)+1188/3=1647/2,
\]
and hence, uniformly in \(|x|\le2\),
\[
 \boxed{|F_x''|<2061/2<1500.}
 \tag{5}
\]
The endpoint regularity in (3) and the sinc representation make (5) valid
at both ends of the interval.

## One midpoint reserve

Let \(u_j=(j+1/2)/N\) and \(q_j=3u_j\), for \(j=0,\ldots,N-1\). Define
the actual finite polynomial
\[
 J_{P,N}(H/2)=\frac12+\Re\sum_j\kappa_j(H)\phi_P(q_j)^4,
\]
\[
 \kappa_j(H)=\frac{(1-u_j)+iR(u_j)}N e^{-iq_jH}.
 \tag{6}
\]
Composite midpoint quadrature and (5) give
\[
 |J_P(x)-J_{P,N}(x)|\le\frac{2061}{48N^2}.
\]
For the raw normalized numerator this is
\[
 \boxed{2|J_P-J_{P,N}|\le\frac{2061}{24N^2}
       =\frac{687}{8N^2}<\frac{125}{N^2}.}
 \tag{7}
\]
If rigorous arithmetic proves
\(2(J_{P,N}(H/2)-\Phi(H/2))\le U_H\) for every law in a specified
moment cell satisfying (1), its positive discrepancy is at most
\[
 \frac{U_H+2061/(24N^2)}\rho.
 \tag{8}
\]
The finite-polynomial bound may use a common signed defect measure,
optimized modulus radii, and exact fourth-power remainders. These are
algebraic bounds at the finitely many frequencies in (6). Neither their
minimum nor their chosen dual multipliers have to vary smoothly with
frequency. Equation (7) controls the entire original physical integral
once; adding separate reference and transfer reserves would be redundant.

## Threshold interpolation and tails

Let \(G_P(x)=2(J_P(x)-\Phi(x))\). Since \(|\phi_P|\le1\),
\[
 |J_P''(x)|\le36\left(\frac1{12}+\frac1{2\pi}\right)<9,
 \qquad |x\phi(x)|<1/4.
\]
Consequently \(|G_P''|<19\), and the raw-threshold function
\(H\mapsto G_P(H/2)\) has curvature at most \(19/4\). For adjacent raw
thresholds at spacing \(h\), linear interpolation needs the raw reserve
\[
 \boxed{19h^2/32.}
 \tag{9}
\]
This interpolates the physical function, not the nonsmooth minimum of
several computed bounds. At each endpoint any separately valid bound may
be used. At \(h=1/32\), (9) is exactly \(19/32768\).

The central grid covers \(H\in[-4,25/8]\). For \(H\le-4\), Cantelli gives
\(P(Z\le H/2)\le1/5\), so the positive normalized score is at most \(2/5\).
For \(H\ge25/8\), the retained Gaussian bound
\(\Phi(25/16)>4/5\) gives the same upper bound. Both signed moment
orientations must be covered: reflection does not turn the closed Prawitz
majorant into its naive complement. The usual closed-CDF reflection
inequality then controls the negative discrepancy too.

## Contact safe integer response computation

For a tagged half-line, \(c=a\) or \(b\), \(y=|x|\), and \(\sigma=\pm1\),
the Hermite response from the
[common measure comparison](n4_Q3_signed_response_constraints_2026_10_08.md)
is \(r_q(\sigma y)=e^{i\sigma q\cdot}[0,c,c,y]\). Put \(R_*=17/4\) and
\[
 h_0=1,\qquad h_n=(y/R_*)h_{n-1}+(n+1)(c/R_*)^n.
\]
Then its truncated series is
\[
 r_q(\sigma y)=\sum_{n=0}^{60}(i\sigma)^{n+3}b_nh_n+E_q,
 \quad b_0=q^3/6,\quad b_n=b_{n-1}(qR_*)/(n+3),
\]
\[
 \boxed{|E_q|\le\frac{q^3}{6}\frac{(qR_*)^{61}}{61!}.}
 \tag{10}
\]
Indeed, Hermite–Genocchi represents the response as \((i\sigma q)^3/6\)
times the expectation of \(e^{i\sigma qV}\), where \(V\) is a convex
combination of \(0,c,c,y\). Thus \(0\le V\le R_*\); the imaginary-exponential
Taylor integral remainder has no exponential growth factor. Its moments
give the complete-homogeneous recurrence above. The normalization prevents
large intermediate powers and removes division at \(y=0,c\).

## Current numerical scope

The separate bounded-support pilot scanned four fixed profiles: the two
values \(w=97/100,9/10\), with \(\beta=\pm3/10\) and their two fixed raw
excesses. It did not cover the full three-dimensional moment root.
At \(N=512\), its largest combined sampled budget was approximately
\(0.403953\); local refinement at \(N=1024\) gave \(0.403977\).
These numbers are ordinary floating diagnostics, not bounds from exact
arithmetic or a CDF certificate.

Independent reconstruction of the absolute-only branch at all 229 dense
thresholds gave approximately \(0.400735\) for \(w=97/100,\beta=3/10\),
but \(0.412361\) for \(w=9/10,\beta=3/10\). The latter profile therefore
still needs the signed common-measure branch at some thresholds. The two
reflected profiles had smaller absolute-only maxima. A successful helper
radius computation alone cannot certify the whole combined gate.

The analytic bridge (1)–(10) was checked independently by both mathematical
auditors. Full completion still requires outward arithmetic for (6),
every central threshold and its interpolation reserve, both orientations,
and a closed cover of all remaining admissible moment cells. No
unrestricted \(C_4\) theorem is asserted here.
