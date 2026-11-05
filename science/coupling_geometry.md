# Coupling geometry beyond a shared scalar profile

The main theorem uses one scalar coefficient for both field axes. The singlet-variance argument identifies why that assumption gives a quadratic achievable scale: all local couplings lie on a one-parameter family. This page derives a related guarantee for several known parameters and for smoothly varying local field directions. It is an achievability statement; the parameter dimension does not determine an optimal lifetime.

## 1. Hermitian one-body fields

Let there be a fixed number $`s`$ of common noise fields, with fixed rates $`\gamma_\ell>0`$ and Hermitian jumps

```math
A_\ell=\sum_{j=1}^n \boldsymbol v_\ell(u_j)\cdot
                    \boldsymbol\sigma_j,
\qquad
\mathcal L=\sum_{\ell=1}^s\gamma_\ell\mathcal D[A_\ell].
\tag{G1}
```

Here $`\boldsymbol\sigma_j=(X_j,Y_j,Z_j)`$, the supplied parameters satisfy $`u_j\in[0,1]^r`$, and each fixed map $`\boldsymbol v_\ell:[0,1]^r\to\mathbb R^3`$ is Lipschitz:

```math
\|\boldsymbol v_\ell(u)-\boldsymbol v_\ell(u')\|_2
\le L_\ell\|u-u'\|_2.
\tag{G2}
```

The integers $`r,s`$, rates, maps and Lipschitz constants do not grow with $`n`$. Define $`\Lambda=\sum_\ell\gamma_\ell L_\ell^2`$. There is no additional Hamiltonian. The boundary operations, classical key and error criterion are those of [the model](model.md).

This includes the main example with $`r=1`$, $`u_j=g_j-1`$, $`\boldsymbol v_x(u)=(1+u)(1,0,0)`$ and $`\boldsymbol v_z(u)=(1+u)(0,0,1)`$. It also permits local polarization directions that vary with $`u`$.

## 2. Exact singlet variance for vector couplings

The singlet moment structure below is inherited; see [Urizar-Lanz et al. (2013), Eqs. (10), (16)–(18)](https://www.gtoth.eu/Publications/PRA13_singlet.pdf).

Let $`P_m`$ project onto the complete singlet sector of an even number $`m`$ of spins, with dimension $`D_m`$. Global rotation and permutation invariance give

```math
\frac{\operatorname{Tr}(P_m\sigma_i^a\sigma_j^b)}{D_m}
=\begin{cases}
\delta_{ab},&i=j,\\
-\delta_{ab}/(m-1),&i\ne j.
\end{cases}
\tag{G3}
```

For different sites, rotation invariance makes the tensor proportional to $`\delta_{ab}`$ and permutation invariance makes the coefficient independent of the pair. Squaring any component of the total spin, which annihilates the singlet sector, fixes that coefficient at $`-1/(m-1)`$. For the same site, the Pauli product rule and the zero one-spin expectation give the first line.

For arbitrary real vectors $`\boldsymbol v_j`$, put
$`A=\sum_{j=1}^m\boldsymbol v_j\cdot\boldsymbol\sigma_j`$
and $`\overline{\boldsymbol v}=m^{-1}\sum_j\boldsymbol v_j`$.
Expanding $`A^2`$ using (G3) gives

```math
\frac{\operatorname{Tr}(P_mA^2)}{D_m}
=\frac{m}{m-1}
  \sum_{j=1}^m\|\boldsymbol v_j-\overline{\boldsymbol v}\|_2^2.
\tag{G4}
```

Every one-spin Pauli has zero compression to the singlet sector, so $`P_mAP_m=0`$. If $`Q\le P_m`$ has dimension $`d_m=2^{\lfloor\log_2D_m\rfloor}`$, positivity also gives

```math
\frac{\operatorname{Tr}(QA^2)}{d_m}
\le\rho_m\frac{\operatorname{Tr}(P_mA^2)}{D_m},
\qquad \rho_m=D_m/d_m<2.
\tag{G5}
```

Apply the encoded-Bell survival proof from [the storage theorem](storage_theorem.md). The block Lindblad generator is self-adjoint and negative semidefinite in Hilbert–Schmidt inner product. The spectral Jensen bound and the inverse-on-code, reset-on-leakage decoder therefore imply

```math
p_b\le 1-e^{-t\mu_b}\le t\mu_b,
\qquad
\mu_b=\rho_m\frac{m}{m-1}
\sum_{\ell=1}^s\gamma_\ell
\sum_{j\in b}\left\|
\boldsymbol v_\ell(u_j)-\overline{\boldsymbol v}_{\ell,b}
\right\|_2^2.
\tag{G6}
```

This step does not require the equal-coupling part of a jump to commute with its mismatch. The separate restricted-generator diamond-norm estimate in the scalar proof used that commutation; (G6) uses only singlet variance and the Hermitian-generator spectral argument.

## 3. Parameter-space grouping

Choose an even $`m`$ and $`C>1`$, and partition each parameter coordinate into

```math
B=\left\lfloor\left(\frac{n}{Cm}\right)^{1/r}\right\rfloor
```

equal intervals. There are $`B^r`$ cells. Form complete $`m`$-spin blocks in each cell. Fewer than $`B^r(m-1)\le n/C`$ spins are omitted.

The squared distance of a parameter from its cell midpoint is at most $`r/(4B^2)`$. The mean vector minimizes the sum of squared distances, so (G2) and (G6) give

```math
\mu_b\le
\rho_m\frac{m^2}{m-1}\frac{r\Lambda}{4B^2}.
\tag{G7}
```

When $`n\ge 2^rCm`$, the elementary bound on the floor yields

```math
\mu_b\le
\rho_m\frac{m^2}{m-1}\,r\Lambda
\left(\frac{Cm}{n}\right)^{2/r}.
\tag{G8}
```

Each jump is still a sum of Hermitian operators on separate sites. The partial-trace identity, exact block marginals, Pauli twirl and correlated-error recovery argument are unchanged. An outer code correcting a fraction $`q`$ of its logical input positions consequently has the sufficient bound

```math
\epsilon_{\mathrm{mem}}
\le \frac{t}{q}\,
\rho_m\frac{m^2}{m-1}\,r\Lambda
\left(\frac{Cm}{n}\right)^{2/r},
\tag{G9}
```

with integer thresholds handled as in the finite-size theorem.

For every fixed rate $`0<R<1`$ and error $`\epsilon>0`$, choose fixed block, discard and outer-code parameters. Equation (G9) then permits $`t=c_{R,\epsilon}n^{2/r}`$. Existing fixed-rate Tanner codes give the same polynomial endpoint construction as in [resources](resources.md), provided evaluation and certified grouping of the supplied parameters are computationally available. The storage bound itself does not assume an efficient oracle for arbitrary real functions.

For every $`t_n=o(n^{2/r})`$, rate one and vanishing error are also achievable existentially. To make the limit explicit, set

```math
s_n=\frac{n^{2/r}}{1+t_n},\qquad
u_n=\min\{s_n^{1/(4+8/r)},\log n\}.
```

Take $`C\asymp u_n`$, even $`m\asymp u_n`$, and $`q\asymp u_n^{-1}`$. The error in (G9) is $`O(u_n^{2+4/r}/s_n)=O(s_n^{-1/2})`$, while the retained fraction, inner singlet rate and outer distance-code rate all approach one. The floor conditions hold for sufficiently large $`n`$.

## 4. Consequences and limits

| Coupling family | Sufficient growing-time regime at rate approaching one |
|---|---|
| One common scalar amplitude for the two axes | $`t_n=o(n^2)`$ |
| Any fixed Lipschitz one-parameter family, including varying local directions | $`t_n=o(n^2)`$ |
| Two independently specified bounded scalar amplitudes for fixed $`X`$ and $`Z`$ axes | $`t_n=o(n)`$ |
| A fixed $`r`$-parameter Lipschitz family | $`t_n=o(n^{2/r})`$ |

These are lower bounds on achievable storage, not matching exponents. A redundant parameterization can give a weaker bound than a lower-dimensional description of the same family. Exact degeneracies or other structure may allow much longer memory.

The [full-algebra proposition](symmetry.md) is proved for the original distinct scalar coefficients. It is not automatically asserted for every vector family in (G1). Conversely, the storage proof does not require irreducibility. The finite number of common fields and the fixed parameter complexity are essential to this corollary; an independent noise field for each spin does not satisfy those assumptions.

[Scientific overview](README.md) · [Scalar storage theorem](storage_theorem.md) · [Interpretation](interpretation.md)
