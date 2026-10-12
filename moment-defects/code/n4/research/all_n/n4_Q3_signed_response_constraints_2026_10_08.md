# Signed Fourier response and realizable Q3 defect measures

For an arbitrary standardized law with a finite third absolute moment, the
same Q3 defect measure represents every characteristic function error.
Its positivity alone is insufficient: matching the sign moments imposes
inverse-size budgets and exact linear balance conditions. These constraints
give signed Fourier bounds and a sharper fourth-power remainder. They do
not by themselves prove an unrestricted fourth-index Berry–Esseen bound.

## Reference and common response

Let \(EX=0\), \(EX^2=1\), and \(\rho=E|X|^3<\infty\). Set
\[
 u=EX_+=EX_->0,\quad v_\pm=EX_\pm^2,\quad
 b=v_+/u,\quad a=v_-/u,
\]
\[
 p_+=u/b,\quad p_-=u/a,\quad p_0=1-p_+-p_-\ge0,
 \qquad Q=p_-\delta_{-a}+p_0\delta_0+p_+\delta_b.
\]
The raw excess and its nonnegative weight are
\[
 W(x)=x_+(x-b)^2+x_-(x+a)^2,\qquad
 \eta=EW=\rho-(v_+^2+v_-^2)/u.
\]
If \(\eta=0\), then \(P=Q\), including its possible zero atom. Otherwise
\(d\nu=W\,dP/\eta\) is a probability measure supported off
\(Z=\{-a,0,b\}\).

On the half-line tagged by \(\sigma\in\{+1,-1\}\), write \(y=|x|\)
and \(c=b\) or \(a\), respectively. For \(f(y)=e^{i\sigma qy}\), let
\[
 H(y)=1+\alpha y+\beta_H y^2,\quad
 \alpha=\frac{2(f(c)-1)-cf'(c)}c,\quad
 \beta_H=\frac{cf'(c)-f(c)+1}{c^2}.
\]
This is the quadratic Hermite interpolant at \(0,c,c\). Define
\[
 r_q(\sigma y)=\frac{f(y)-H(y)}{y(y-c)^2}=f[0,c,c,y].
\]
The limits at the removable contacts are
\[
 r_q(\sigma0)=\frac{f'(0)-\alpha}{c^2},\qquad
 r_q(\sigma c)=\frac{f''(c)/2-\beta_H}{c}.
\]
The two tagged limits at zero need not agree. They must not be identified
in a numerical response curve. Actual \(\nu\) gives no mass to these contacts.
Since the Hermite polynomial preserves the sign moments,
\[
 \boxed{\phi_P(q)-\phi_Q(q)=\eta\int r_q(x)\,d\nu(x).}
 \tag{1}
\]

The Hermite–Genocchi formula integrates \(f'''\) over the three-dimensional
simplex of volume \(1/6\). Differentiation with respect to its last node
introduces its barycentric coordinate, whose integral is \(1/24\). Thus
\[
 |r_q|\le |q|^3/6,\qquad |\partial_y r_q|\le |q|^4/24.
 \tag{2}
\]
This differentiates a deterministic exponential, not an expectation of
\(X^4\); no fourth moment is required.

## Exact feasibility conditions

The cardinal functions
\[
 \ell_0=1-X_+/b-X_-/a,\quad
 \ell_+=X_+/b,\quad \ell_-=X_-/a
\]
have the same second-moment matrix under \(P\) and \(Q\):
\[
 E_P[\ell\ell^\top]=\operatorname{diag}(p_0,p_+,p_-).
\]
Indeed, \(E\ell_+^2=v_+/b^2=u/b\),
\(E\ell_0\ell_+=u/b-v_+/b^2=0\), and the other entries follow by reflection
and \(\ell_0+\ell_++\ell_-=1\). Splitting off the three contact atoms gives
\[
 \boxed{\operatorname{diag}(p_0,p_+,p_-)
 -\eta\int\frac{\ell(x)\ell(x)^\top}{W(x)}\,d\nu(x)
 =\operatorname{diag}(P\{0\},P\{b\},P\{-a\})\succeq0.}
 \tag{3}
\]
All entries are integrable for an actual law, because the weighted integral
is exactly an expectation over \(P\) off \(Z\).

On a tagged half-line, \(\ell_0^2/W=1/(c^2y)\). The first diagonal entry
therefore proves the particularly simple positive budget
\[
 \boxed{\eta\int\frac{1}{c^2y}\,d\nu=p_0-P\{0\}\le p_0.}
 \tag{4}
\]
The off-diagonal entries give
\[
 \int_{x>0}\frac{d\nu}{x-b}=0,\qquad
 \int_{x<0}\frac{d\nu}{-x-a}=0,
 \tag{5}
\]
and the other diagonal entries give
\[
 \eta\int_{x>0}\frac{d\nu}{(x-b)^2}\le u,\qquad
 \eta\int_{x<0}\frac{d\nu}{(-x-a)^2}\le u.
 \tag{6}
\]
These conditions eliminate many response measures that positivity alone
would permit. A free signed multiplier for (5) has a pole at a contact;
finite dual envelopes must control it, for example using (6).

More explicitly, on the tag with radius \(c\),
\[
 \eta\int_{\rm tag}\frac{d\nu}{(y-c)^2}
 =E[y;\ X\text{ is on this tag and }y\ne c]
 =u-cP\{\sigma c\}\le u,
\]
\[
 \eta\int_{\rm tag}\frac{d\nu}{y-c}
 =E[y(y-c);\ X\text{ is on this tag}]=v_{\rm tag}-cu=0.
\]
The pole is absolutely integrable because \(y|y-c|\le y^2+cy\).

For a real response \(K\), let
\[
 k_0(\sigma y)=1/(c_\sigma^2y),\quad
 k_2(\sigma y)=1/(y-c_\sigma)^2,\quad
 k_1(\sigma y)=1/(y-c_\sigma).
\]
For \(\lambda_0,\lambda_+,\lambda_-\ge0\) and arbitrary real
\(\theta_+,\theta_-\), the same measure therefore satisfies
\[
 \boxed{\eta\int K\,d\nu\le
 \lambda_0p_0+u(\lambda_++\lambda_-)
 +\eta\sup_{\sigma,y}
 \left(K(\sigma y)-\lambda_0 k_0(\sigma y)
       -\lambda_\sigma k_2(\sigma y)-\theta_\sigma k_1(\sigma y)\right).}
 \tag{6a}
\]
This uses two inverse-square budgets and both exact sign balances in
addition to the zero-mass budget. It is applicable to a signed Fourier
curve or to \(K=|r_q|\). No additional moment or realizability assumption
is introduced.

If \(\theta_\sigma\ne0\), a positive \(\lambda_\sigma\) controls its pole.
Writing \(z=1/(y-c_\sigma)\),
\[
 -\lambda_\sigma z^2-\theta_\sigma z
 \le\theta_\sigma^2/(4\lambda_\sigma).
\]
On a cell crossing the contact, its reciprocal domain is the union of
two rays, not the whole real line. The exact concave quadratic maximum
on each ray is obtained at its endpoint or at the vertex if the vertex
lies on that ray. Combining this upper bound with a response Lipschitz
margin and the lower \(k_0\) cost gives a contact-safe cell enclosure.
For interval-valued excess, multiplication of a negative supremum uses
the lower excess endpoint; the upper endpoint is valid only for a
nonnegative supremum.

For completeness, an off-contact probability measure \(\nu\) is realizable
at the prescribed \(u,a,b,\eta>0\) exactly when there are nonnegative masses
\(\pi_-,\pi_0,\pi_+\) and the following finite integrals:
\[
 \eta\int W^{-1}\,d\nu+\pi_-+\pi_0+\pi_+=1,
\]
\[
 \eta\int x_+/W\,d\nu+b\pi_+=u,\quad
 \eta\int x_+^2/W\,d\nu+b^2\pi_+=v_+,
\]
with the reflected pair on the negative side. Necessity follows from
\(P_{\rm off}=\eta\nu/W\). Conversely, these equations construct a
probability law with the required first two sign moments. Its third moment
is finite and equals \((v_+^2+v_-^2)/u+\eta\), because the pointwise identity
\(|x|^3=W(x)+2b x_+^2-b^2x_++2a x_-^2-a^2x_-\) is integrable.

In fact the three budgets and two balances above already characterize
this entire moment fibre. Fix \(u,a,b\) with \(u(a+b)=1\) and
\(p_0=1-u/a-u/b\ge0\), and fix \(\eta>0\). Let \(\nu\) be a probability
measure off the three contacts. Suppose
\[
 \eta E_\nu k_0\le p_0,\qquad
 \eta E_\nu[\mathbf1_{\rm tag\,\sigma}k_2]\le u,\qquad
 E_\nu[\mathbf1_{\rm tag\,\sigma}k_1]=0
 \quad(\sigma=+,-).
 \tag{6b}
\]
Then a realizing law is constructed by
\[
 dP_{\rm off}=\eta W^{-1}d\nu,\qquad
 P\{\sigma c_\sigma\}=\frac{u-\eta E_\nu[\mathbf1_{\rm tag\,\sigma}k_2]}{c_\sigma},
 \qquad P\{0\}=p_0-\eta E_\nu k_0.
 \tag{6c}
\]
To verify this, use on each tag the exact partial fractions
\[
 W^{-1}=k_0-k_1/c^2+k_2/c.
\]
The budgets make \(k_0,k_2\) integrable, while Cauchy makes \(k_1\)
absolutely integrable. The off-contact mass is finite, and (6c) gives
nonnegative contact masses. Their total is one. The first and second
tag moments are \(u\) and \(cu\), since their off-contact contributions
are \(\eta E k_2\) and \(\eta E(k_1+ck_2)\), respectively. Finally,
\[
 E_P[X_\sigma^3]=u c_\sigma^2+\eta\nu(\text{tag }\sigma),
\]
because \(y^3/W=1+2ck_1+c^2k_2\). Thus \(E|X|^3=u(a^2+b^2)+\eta\)
is finite and \(W\,dP/\eta=d\nu\). Necessity was established above.
This proves exact moment-law realizability, even for an unbounded
\(\nu\). A bounded domain for \(\nu\) and its contact nodes gives a bounded
realizing law. It does not impose the separate contact or maximality
conditions of an extremizer. The branch \(\eta=0\) remains \(P=Q_3\).

## A global quadratic cap

The interpolant also satisfies
\[
 H(y)=f(c)+f'(c)(y-c)+\beta_H(y-c)^2,
 \qquad
 \beta_H=c^{-2}\int_0^c zf''(z)\,dz.
\]
Hence \(|\beta_H|\le q^2/2\). Taylor's integral formula at \(c\) yields
\[
 |f(y)-H(y)|\le q^2(y-c)^2,\qquad
 \boxed{|r_q(\sigma y)|\le q^2/y\quad(y>0).}
 \tag{7}
\]
This is also a sharper tail bound than the earlier polynomial tail estimate.
Combining (1), (4), and (7), with \(M=\max(a,b)\), gives
\[
 |\phi_P(q)-\phi_Q(q)|\le M^2p_0q^2.
 \tag{8}
\]
This reproduces the existing quadratic mass-slack bound in
[the earlier combined Hermite estimator](n4_adaptive_Q3_combined_Hermite_quadratic_error_v2_2026_10_04.py),
not a new pointwise characteristic-function estimate. The common response
formulation retains the exact inverse-size budget that proves it.
Thus a safe error radius is
\[
 \epsilon_q=\min\{1+|\phi_Q(q)|,\eta|q|^3/6,M^2p_0q^2\}.
 \tag{9}
\]
Retaining the actual response curve gives a potentially smaller radius:
\[
 |\phi_P(q)-\phi_Q(q)|\le
 \inf_{\lambda\ge0}\left\{\lambda p_0+\eta
   \sup_{\sigma,y>0}\left(|r_q(\sigma y)|-\frac\lambda{c^2y}\right)\right\}.
 \tag{9a}
\]
Indeed, integrate \(|r_q|\), subtract its nonnegative inverse-size cost,
and apply (4). Bounds (9) and (9a) may be combined by taking their minimum.

## Signed fourth-power comparison

For finitely many raw frequencies \(q_j\) and complex weights \(\kappa_j\),
set
\[
 F(P)=\Re\sum_j\kappa_j\phi_P(q_j)^4,\qquad
 A(x)=\Re\sum_j4\kappa_j\phi_Q(q_j)^3r_{q_j}(x).
\]
Then
\[
 F(P)-F(Q)=\eta\int A\,d\nu+\mathcal R.
 \tag{10}
\]
For any \(\lambda\ge0\), (4) implies the one-sided dual bound
\[
 \boxed{\eta\int A\,d\nu\le
 \lambda p_0+\eta\sup_{\sigma,y>0}
 \left(A(\sigma y)-\frac\lambda{c^2y}\right).}
 \tag{11}
\]
The lower bound follows by applying (11) to \(-A\). In particular, one
must maximize the signed common curve, not a separate modulus at every
frequency. Any chosen nonnegative multiplier is valid; optimality is not
needed for a certificate.

The global Lipschitz constant of \(A\) is at most
\[
 L=\sum_j |4\kappa_j\phi_Q(q_j)^3|\,|q_j|^4/24.
\]
On a nearest-node half-cell of radius \(h/2\) around \(y_i\ge0\),
\[
 A(\sigma y)-\lambda/(c^2y)
 \le A(\sigma y_i)+Lh/2-\lambda/[c^2(y_i+h/2)].
 \tag{12}
\]
This avoids differentiating the singular cost at zero. By (7), on \(y\ge R\)
the absolute curve is at most
\(R^{-1}\sum_j |4\kappa_j\phi_Q(q_j)^3|q_j^2\); dropping the negative
dual cost gives a safe tail upper bound.

For the nonlinear remainder, write \(z=\phi_Q(q)\), \(A_0=\phi_P(q)\),
\(\delta=A_0-z\), and \(r=|z|\). Exactly,
\[
 A_0^4-z^4-4z^3\delta
 =12\delta^2\int_0^1(1-s)(z+s\delta)^2\,ds.
\]
Taking absolute values and evaluating the quadratic integral gives
\[
 |A_0^4-z^4-4z^3\delta|
 \le |\delta|^2(4r^2+2|A_0|^2-|\delta|^2)
 \le |\delta|^2(4r^2+2-|\delta|^2).
\]
The last quadratic in \(|\delta|^2\) has its maximum at \(2r^2+1\). Thus,
for \(U=\min(\epsilon_q^2,2r^2+1)\), a safe remainder cap is
\[
 B_q=\min\{6r^2\epsilon_q^2+4r\epsilon_q^3+\epsilon_q^4,
                  U(4r^2+2-U)\},
 \qquad |\mathcal R|\le\sum_j|\kappa_j|B_{q_j}.
 \tag{13}
\]
This uses the characteristic-function unit disk and the exact iid fourth
power, not a dependent-product relaxation.

The common measure can also retain the signed second-order term. With
\(g_j=\phi_Q(q_j)\), define
\[
 A_1(x)=\Re\sum_j4\kappa_jg_j^3r_j(x),\qquad
 A_2(x,y)=\Re\sum_j6\kappa_jg_j^2r_j(x)r_j(y).
\]
There is no complex conjugation in \(A_2\). The exact expansion is
\[
 F(P)-F(Q)=\eta E_\nu A_1+\eta^2E_{\nu\otimes\nu}A_2+\mathcal R_{34}.
\]
For \(p_j=\min(1,|g_j|+\epsilon_j)\),
\[
 |\mathcal R_{34}|\le\sum_j|\kappa_j|\epsilon_j^3(3|g_j|+p_j),
 \tag{13a}
\]
since \(4g\delta^3+\delta^4=\delta^3(3g+\phi_P)\).
For the cost
\(b(x)=\lambda_0k_0(x)+\lambda_\sigma k_2(x)+\theta_\sigma k_1(x)\),
set \(B=\lambda_0p_0+u(\lambda_++\lambda_-)\). The pair dual is
\[
 \eta^2E A_2\le2\eta B+
       \eta^2\sup_{x,y}[A_2(x,y)-b(x)-b(y)].
 \tag{13b}
\]
The budget factor is \(2\eta\), not \(2\eta^2\). Both first orders may
instead be optimized together by replacing \(\eta^2 A_2\) in the
supremum by
\(T_\eta=\eta(A_1(x)+A_1(y))/2+\eta^2A_2(x,y)\), and subtracting
\(\eta^2(b(x)+b(y))\). This still uses the same \(2\eta B\) budget.

In each spatial coordinate the Lipschitz constant of \(A_2\) is at most
\[
 L_2=\sum_j|\kappa_j||g_j|^2|q_j|^7/24.
\]
Indeed, differentiate one response and use (2) on the other. On a
rectangle of half-widths \(h_x/2,h_y/2\), the response margin is
\(L_2(h_x+h_y)/2\). Pole costs are enclosed separately as above.
These are analytic ingredients for a two-dimensional signed certificate,
not a numerical improvement already incorporated in a CDF receipt.

## Pilot results and the remaining smoothing step

The finite Fourier-polynomial pilot used the two preselected charts
\((w,\beta)=(97/100,3/10),(9/10,3/10)\), with excesses
\(1633550843/10796617633\) and \(113089567/365551652\). Its 24 positive
normalized frequencies were \(t_j=j/12\), with raw \(q_j=t_j/2\), and
\[
 \kappa_j=\frac{i}{12\pi t_j}
   e^{-t_j^2/(2T^2)}e^{-it_jH}.
\]
The three widths and five thresholds were fixed before evaluation. Relative
to a triangle sum, the sampled full-error estimates improved by factors
between 1.01 and 4.28. Common signed frequency information alone improved
the corresponding separate signed linear estimates by factors up to 1.34. At
\(H=0\), the full improvement was only 1.13–1.35, so the largest gain must
not be represented as uniform in the threshold.

Seventeen finite-law regressions checked (1), (4), and the quartic expansion;
the largest response identity error was below \(4\cdot10^{-16}\). These
are floating regressions, not outward-rounded certificates. The recorded
mesh and tail margins do not certify floating evaluation errors. The pilot
used the older, weaker tail and triangle remainder; (7), (9), and (13) were
derived afterwards and are not claimed as incorporated in that receipt.

The polynomial is a smooth bounded test, not a CDF majorant. A Berry–Esseen
application must still insert the actual one-sided smoothing kernel, cover
the entire frequency integral, include the smoothing cost at atoms, and
control every threshold and parameter cell. No new cutoff, unrestricted
index, or Lean theorem follows from this pilot.

## Sources

The Q3 moment construction and exact third-order smooth metric are in
[the existing adaptive comparison](adaptive_three_point_fourier_comparison_2026_10_04.md).
The common Fourier ledger and its frequency regularity are in
[the Q3 Gram note](n4_Q3_shared_sample_gram_lemmas_2026_10_08.md).
The independent proof audits were supplied by the two mathematical agents.
The concrete floating pilot is retained in
[its result](n4_Q3_signed_joint_response_pilot_2026_10_08.json).
These are local derivations using classical Hermite interpolation and dual
bounds; no global novelty or imported Berry–Esseen theorem is asserted.
