# Elementary radius 17/4 at a first critical index

1 October 2026. This is a conditional structural reduction, not a proof
that any remaining finite-index Berry--Esseen constant is below `C_E`.
It uses no solver, finite-support assumption, local certificate, or
fourth moment. All decimals in the cited inequalities are exact rationals.

## Statement and input boundary

Let `m>=4` be an integer with `C_{m-1}<C_E<=C_m`. Let `(P,H)` be the
attained, positively oriented closed maximizing pair for `C_m`,
standardized by `EX=0`, `EX^2=1`; write `rho=E|X|^3`,
`beta=E[X|X|]`, and `C=C_m`. Then

```text
supp(P) subset (-17/4,17/4).
```

The *external* analytic inputs are the published iid normalized
Berry--Esseen envelope
`C_m<=.3031*(rho+.646)/rho`, the finite Gaussian estimate (70) of
He--Cheng, and their finite contamination-contact identity (Lemma 4.3).
Critical-level attainment, including `C_m=C_E`, and contact on the
**whole closed support** are the separately established project inputs
in `critical_level_attainment.md`. The grouping, covariance bound,
and exact radius calculation below are the new deductions here.
The original He--Cheng first-supercritical selection is not used to
justify equality-level attainment.

## Exact preliminary bounds

Put `c=256/625=.4096`. The elementary estimates
`pi<22/7` and `sqrt(10)>1581/500` give

```text
C_E^2=(19+6sqrt(10))/(72pi)
  >66451/396000>(256/625)^2,
```

where the last comparison has cross-product difference `5165875>0`.
Thus `C>=C_E>c`. Also `phi(0)<2/5`, since `pi>25/8`.

The published `.3031` envelope and `C>c` imply

```text
rho < [(.3031)(.646)]/(c-.3031)
    =979013/532500<46/25;
```

the last cross-product margin is `19675>0`.
There is an additional all-law signed-moment gain. Cauchy and
interpolation give

```text
|beta|^2 <= Var(X) Var(|X|)=1-(E|X|)^2,
1=E|X|^2 <= sqrt(E|X| * rho),
```

so `|beta|^2<=1-1/rho^2<1491/2116<441/625`, the last exact
cross-product gap being `1281>0`. Therefore `|beta|<21/25`.

Let `s_m=sqrt(m/(m-1))`. The identity
`m(s_m-1)=s_m^2/(s_m+1)` shows that this expression decreases in
`m`; at `m=4`, it is below `5/8`, because
`sqrt(4/3)<37/32` is equivalent to `4096<4107`.
It is also above `1/2`, since `s_m>1` and
`2s_m^2-s_m-1=(2s_m+1)(s_m-1)>0`.
Thus `1/2<m(s_m-1)<5/8` for all `m>=4`.

## Contact and the polynomial sign

The exact contact identity, the predecessor CDF comparison, and the
Gaussian estimate (70) give, for every real `y`, `r=|y|`,

```text
rho*I(y) <= (phi(0)/6)*r^3+r/5+1/2
            +rho*m(C_{m-1}-C)
            +rho*m(s_m-1)*C_{m-1}
            +C[-r^3+(3/2)*rho*r^2+3*beta*y-rho/2].
```

Since `C_{m-1}<C`, the predecessor difference is negative. Dropping
it and replacing `C_{m-1}` by `C` in the positive scale term gives

```text
rho*I(y) < (phi(0)/6)*r^3+r/5+1/2+C*B_actual(r),
B_actual(r)=-r^3+(3/2)*rho*r^2+3*beta*y
                  +rho*[m(s_m-1)-1/2].
```

For `r>=4`, the preliminaries bound this bracket by

```text
B_actual(r) < B(r):=-r^3+(69/25)*r^2+(63/25)*r+23/100.
```

Here `B(4)=-953/100<0`, `B'(4)=-117/5<0`, and
`B''(r)=-6r+138/25<0` for `r>=4`; hence `B(r)<0` on the
whole ray. **Only because the bracket is negative**, `C>c` may be
used as an upper bound `C*B_actual(r)<c*B(r)`.
With `phi(0)<2/5` we obtain

```text
rho*I(y) < P(r)
 =-(643/1875)*r^3+(17664/15625)*r^2
   +(19253/15625)*r+37138/62500.
```

At `r=17/4`, exact arithmetic gives

```text
P(17/4)   =-224651/3000000<0,
P'(17/4)  =-1935323/250000<0,
P''(17/4) =-202619/31250<0.
```

Since `P''(r)` decreases thereafter, `P(r)<0` for all `r>=17/4`.
The finite contact theorem says `I(y)=0` at **every point of the
closed support** of the attained maximizer. Thus no support point,
including an atom or accumulation point, has `|y|>=17/4`, proving
the claimed strict open support interval.

This is stronger than the earlier elementary first-critical radius
`97/20` and does not use Shevtsova's separate `.469` cap. The
preserved exact support certificate in the imported cutoff-49 package
still gives the sharper `96/25=3.84` radius when `m>=36` and the
decrement is at most `.19`; at a first critical index the decrement is
zero. Neither support bound by itself excludes that critical index.
The theorem above has no upper-index cutoff: it holds for every first
critical `m>=4` wherever the stated critical-attainment/contact inputs
apply (they are recorded for every integer `m>=2`).
