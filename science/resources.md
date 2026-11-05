# Calibration, code construction, and endpoint resources

This account separates the information-theoretic storage theorem from two constructive implementations. The model, normalization, and allowed classical records are specified in [the operational model](model.md). No quantum system other than the selected physical spins carries information across the storage interval.

| Statement | Endpoint construction | What is controlled |
|---|---|---|
| Rate tending to one for every $`t_n=o(n^2)`$ | General outer distance codes, or deterministic expurgation | Existence and reference-uniform error; no uniform efficient decoder is asserted |
| Every fixed rate $`R\lt 1`$ for $`t\le c_{R,\epsilon}n^2`$ | Fixed-parameter quantum Tanner codes | Polynomial classical construction and endpoint circuits; efficient final classical decoding with perfect syndromes |
| Rate tending to one for $`t_n=o(n^2/\log^3 n)`$ | Growing-field CSS Reed–Solomon codes | A uniform polynomial endpoint construction, with the extra logarithmic loss shown below |

The keyed implementations average over freshly sampled classical Pauli keys and discard the key after recovery. Their output guarantee is a half-diamond bound on the resulting logical channel. They do not assert the same bound for every fixed key. The key contains no quantum information and uses at most two classical bits per inner logical qubit.

## 1. The inner-block interface

Fix an even block size $`m\ge4`$. Let

```math
D_m=\frac{1}{m/2+1}\binom{m}{m/2},\qquad
k_m=\lfloor\log_2D_m\rfloor,\qquad
d_m=2^{k_m},\qquad
\rho_m=\frac{D_m}{d_m}\lt 2.
```

Choose a specified $`d_m`$-dimensional subspace of the spin-zero sector, with an isometry from $`k_m`$ logical qubits. The same isometry can be used in every block. After storage, its inverse is applied on the code subspace; leakage is mapped to a fixed logical state. Every outcome is included.

Write $`\Gamma=\gamma_x+\gamma_z`$. For numerical certificates, every occurrence of $`\Gamma`$ may be replaced by a supplied rational upper bound $`\Gamma_+\ge\Gamma`$. The target storage time and error budgets are supplied as rational numbers as well. For block $`b`$, let $`\bar g_b`$ be the true mean coupling in that block. The inner decoded channel has entanglement infidelity bounded by

```math
p_b\le 1-e^{-t\mu_b}\le t\mu_b,\qquad
\mu_b=\Gamma\rho_m\frac{m}{m-1}
       \sum_{j\in b}(g_j-\bar g_b)^2.
\qquad\text{(R1)}
```

The [storage theorem](storage_theorem.md) proves (R1) by Hilbert–Schmidt spectral Jensen and the full-singlet second moment. This bound applies to any fixed choice of the $`d_m`$ singlet vectors. It does not require optimizing an exponentially large code basis. The factor $`\rho_m`$ is essential: the estimate uses positivity to compare the trace over the selected subspace with the trace over the full singlet sector. Replacing $`d_m`$ by a much smaller dimension can increase this factor.

Independent Pauli conjugations of the inner logical qubits turn the full logical channel into a generally correlated Pauli channel. If $`p=\max_b p_b`$, each logical qubit has nonidentity Pauli probability at most $`p`$. Consequently any selected set of $`N`$ logical positions has expected Pauli weight at most $`Np`$. This statement remains valid when a selected set uses only some of the logical qubits of an inner block.

## 2. Exact grouping from certified finite data

The input consists of rational estimates $`\widehat g_j`$ and rational certificates $`u_j\ge0`$ such that the fixed physical couplings satisfy

```math
g_j\in[a,b],\qquad |g_j-\widehat g_j|\le u_j,
\qquad W=b-a>0.
```

These are supplied calibration assumptions. The construction does not infer the certificates from experimental samples.

Choose a dyadic grid spacing $`h`$. Round each estimate to a nearest grid point, using a specified tie rule, and project the result onto $`[a,b]`$. Call the result $`\widetilde g_j`$. Projection onto this interval cannot increase the distance to its true coupling, so

```math
|g_j-\widetilde g_j|\le u_j+h/2=:\eta_j,
\qquad \eta=\max_j\eta_j.
\qquad\text{(R2)}
```

For a discard parameter $`C>1`$, use

```math
B=\left\lfloor\frac{n}{Cm}\right\rfloor
```

equal bins, assuming $`n\ge2Cm`$. Their width is $`w=W/B`$. The bin index is computed by exact rational arithmetic as

```math
\min\left\{B-1,\left\lfloor
       \frac{B(\widetilde g_j-a)}{W}\right\rfloor\right\}.
```

Within each bin, take consecutive groups of $`m`$ indices in a fixed ordering. If $`K`$ complete blocks are retained, then

```math
Km\ge n-B(m-1)\ge (1-1/C)n,
\qquad M=Kk_m.
\qquad\text{(R3)}
```

The unused spins are not a clean quantum resource. The common-field channel has closed marginals on the retained spins, so their state does not have to be protected.

For the midpoint $`c_b`$ of the estimated bin, compute the certificate (using $`\Gamma_+`$ for rational computation)

```math
V_b^{\rm cert}
=\sum_{j\in b}\bigl(|\widetilde g_j-c_b|+\eta_j\bigr)^2,
\qquad
\mu_b^{\rm cert}
=\Gamma\rho_m\frac{m}{m-1}V_b^{\rm cert}.
\qquad\text{(R4)}
```

The true mean minimizes the sum of squared deviations. Thus $`\mu_b\le\mu_b^{\rm cert}`$, and $`p_b\le\min\{1,t\mu_b^{\rm cert}\}`$ is a certified bound for every true coupling list consistent with the input. A convenient uniform estimate is

```math
p\le \Gamma t\rho_m\frac{m^2}{m-1}(w/2+\eta)^2.
\qquad\text{(R5)}
```

For $`n\ge2Cm`$, the bin width obeys $`w/2\le WCm/n`$. If $`\eta\le\chi/n`$, then

```math
p\le
\Gamma\rho_m\frac{m^2}{m-1}
       (WCm+\chi)^2\frac{t}{n^2}.
\qquad\text{(R6)}
```

At fixed block and discard parameters, certified accuracy of order $`1/n`$ therefore preserves the quadratic lifetime. Bounded couplings need $`O(\log n)`$ fractional bits at this accuracy. If the supplied uncertainties are larger, the compiler uses (R4) or reports the accuracy needed for the requested certificate; it cannot silently reduce them. The bit count does not price physical calibration time or sample complexity.

No coupling-dependent quantum arithmetic is needed. The estimates determine a classical assignment of physical spin labels to blocks. A circuit description explicitly addresses those spins; arbitrary-position gates, or their routing cost, belong to the endpoint model. No coherent data loader or QRAM oracle is assumed.

## 3. A fixed-rate Tanner outer family

### The inherited coding theorem

Choose a fixed $`\theta\in(0,1/2)`$. Quantum Tanner codes have rate at least $`r_T=(1-2\theta)^2`$ after choosing sufficiently large constant expansion degree $`\Delta`$ and suitable constant-length local codes. The construction and existence of suitable local codes are given in Leverrier–Zémor, [*Quantum Tanner codes*, Theorems 17–18](https://arxiv.org/html/2202.13641v3).

Use the stronger product-expansion hypotheses in Leverrier–Zémor, [*Decoding quantum Tanner codes*, Section 2.7 and Theorem 6](https://arxiv.org/html/2208.05537v3). Let $`\delta_T>0`$ bound the relative distances of the local codes and their duals, and let $`\kappa_T>0`$ be a common product-expansion constant. For any fixed decoder parameter $`\varepsilon_d\in(0,1)`$, their Theorem 13 corrects every Pauli component of weight less than $`q_TN`$, where

```math
q_T=\frac1{2^{11}}
\min\left\{\frac{\varepsilon_d^3}{16},\kappa_T\right\}
(1-\varepsilon_d)\delta_T^2\kappa_T^2\frac1\Delta>0.
\qquad\text{(R7)}
```

Both components are decoded, so a Pauli of total weight less than $`q_TN`$ is corrected. The sequential decoder takes linear time in the code length in the fixed-parameter word-operation model. Theorem 20 also supplies a parallel decoder with its own, slightly smaller threshold. The construction here uses Theorem 13 and perfect final syndromes.

For fixed $`\theta`$, all local codes and local decoder tables have constant size with respect to $`n`$. They can be selected once by finite exhaustive search, checking distances and both product-expansion inequalities, then stored with the family. Existence follows from the random-local-code theorem. This is a potentially very expensive constant setup step, not a claim that code selection is efficient as $`\theta\to0`$. In particular, the construction is uniform in register size after fixed target-rate parameters have been selected.

### Available lengths and an all-size repair

The quadripartite construction uses $`G_i=\mathrm{PSL}_2(q^i)`$ for a fixed odd prime power $`q`$ and $`\Delta=q+1`$. Dinur et al., [arXiv:2111.04808v2, Claim 6.7 and Section 6.2](https://arxiv.org/pdf/2111.04808), supply the explicit generating sets for each sufficiently large $`i`$. A square is specified by one vertex in $`V_{00}`$ and a pair of generators, so its Tanner code length is

```math
N_i=\Delta^2|G_i|
   =\frac{\Delta^2}{2}q^i(q^{2i}-1).
```

Discard finitely many initial lengths if necessary. Consecutive lengths satisfy

```math
\frac{N_{i+1}}{N_i}
=q^3\frac{1-q^{-2(i+1)}}{1-q^{-2i}}
\le L,\qquad L=2q^3.
\qquad\text{(R8)}
```

To use an arbitrary available length $`M`$, repeatedly select the largest admissible $`N_i`$ no larger than the remaining length. Stop after a fixed number $`J`$ of chunks or when fewer than $`N_{\min}`$ positions remain. Whenever a chunk can be chosen, it consumes at least a fraction $`1/L`$ of the remainder. Hence the total used length $`M_{\rm used}`$ obeys

```math
M_{\rm used}\ge
\bigl[1-(1-1/L)^J\bigr]M-N_{\min}.
\qquad\text{(R9)}
```

The $`J`$ chunks use independent Tanner encoding and final recovery, while their input may be entangled across chunks. No independence of storage errors is imposed. Markov's inequality and a union bound give

```math
\epsilon_{\rm storage}
\le\min\left\{1,\frac{Jp}{q_T}\right\}.
\qquad\text{(R10)}
```

Indeed, each chunk of length $`N_i`$ has expected Pauli weight at most $`N_ip`$. Except on an event of probability at most $`p/q_T`$, its Pauli has weight below the decoder threshold. On the joint success event all chunks act as the identity, including on reference-entangled inputs. The remaining branch is a channel, giving the same failure probability as a half-diamond bound.

The total number $`k_{\mathrm{out}}`$ of stored qubits consequently satisfies

```math
\frac{k_{\mathrm{out}}}n
\ge r_T\bigl[1-(1-1/L)^J\bigr]
       (1-1/C)\frac{k_m}{m}-O(1/n).
\qquad\text{(R11)}
```

For any fixed target $`R\lt 1`$, choose fixed $`m,C,\theta,J`$ so that the main coefficient in (R11) exceeds $`R`$. Combining (R6) and (R10), the sufficient storage condition is

```math
t\le
\frac{\epsilon_{\rm storage}q_T(m-1)}
 {J\Gamma\rho_m m^2(WCm+\chi)^2}\,n^2.
\qquad\text{(R12)}
```

All constants are explicit once a particular fixed Tanner family is selected. They may be very poor at high target rate. Keeping $`J`$ fixed matters: filling the register with a growing number of chunks would change the error accounting.

## 4. Endpoint circuit and classical computation accounting

The following algorithms specify a polynomial construction; they are not a claim that a practically sized Tanner instance has been optimized or that a hardware compiler has been implemented in this repository.

1. Read and round the certified coupling list. Form bins and complete inner blocks using integer and rational arithmetic. Record their physical spin indices.
2. Generate the at most $`J`$ Tanner complexes and sparse CSS check matrices. Their finite fields have degree $`O(\log n)`$ over a fixed base field. The published generator construction and group arithmetic take polynomial time. Even exhaustive irreducible-polynomial search at these field sizes is polynomial in the resulting code length.
3. Put the CSS stabilizer into standard form by binary linear algebra. Record an encoder, logical operators, and the sparse checks needed by the Tanner decoder.
4. Apply the outer Clifford encoder, then the sampled Pauli keys, then each inner isometry. All temporary quantum workspace is reset or discarded before storage.
5. After storage, decode each inner block, applying the specified reset on leakage. Invert the keys, measure the outer CSS syndromes, run the two classical Tanner decoders, apply their Pauli corrections, and apply the inverse outer encoder. Output a fixed valid state on any declared decoder-failure branch.

For a chunk of $`N`$ qubits and $`k`$ logical qubits, Gottesman, [*Stabilizer Codes and Quantum Error Correction*, Section 4.2, Eq. (4.26)](https://arxiv.org/html/quant-ph/9705052v1), gives an encoding network with at most $`N(N-k)`$ two-qubit operations, plus $`O(N)`$ single-qubit operations. Reversing it after correction decodes the code. Thus the total outer encoder and inverse encoder need $`O(M^2)`$ Clifford gates. A conservative binary linear-algebra preprocessing bound is $`O(M^3)`$ bit operations, apart from index bookkeeping.

For the inner map, enumerate an orthonormal angular-momentum coupling basis, choose the first $`d_m`$ singlets in a specified ordering, and extend to a unitary on the $`m`$ spins. Its Clebsch–Gordan coefficients are computable from finite arithmetic and square roots. A generic unitary decomposition gives the conservative cost

```math
G_{\mathrm{inner}}^{(0)}
=O\bigl(K\,\mathrm{poly}(m)4^m\bigr)
```

in arbitrary single-qubit rotations and two-qubit gates; no table lookup is counted as a unit-time quantum operation. At fixed $`m`$ this is linear in $`n`$. This generic synthesis estimate follows from standard finite-unitary decomposition; see Barenco et al., [*Elementary gates for quantum computation*](https://arxiv.org/abs/quant-ph/9503016). It is sufficient here without an optimized Schur-transform implementation.

Applying the inverse inner unitary and testing its $`m-k_m`$ padding qubits implements the code/leakage test. The failure branch discards and prepares the fixed logical state. These are endpoint operations and use at most linear total ancillary space.

| Resource | Fixed-rate Tanner construction |
|---|---|
| Physical quantum carrier during storage | At most $`n`$ noisy spins |
| Reliable Pauli key during storage | $`2M\le2n`$ classical bits |
| Coupling input at accuracy $`O(1/n)`$ | $`O(n\log n)`$ bits for bounded coefficients |
| Block assignment and sparse code description | $`O(n\log n)`$ bits for fixed family parameters |
| Dense stabilizer preprocessing | A conservative $`O(n^3)`$ binary-operation bound |
| Ideal outer encoder and inverse | $`O(n^2)`$ Clifford gates |
| Ideal inner encoding and decoding | $`O(n)`$ gates with constants depending on $`m`$ |
| Perfect outer syndrome extraction | $`O(n)`$ gates and preparations for fixed LDPC parameters |
| Final classical Tanner decoding | $`O(n)`$ word operations; polynomial bit complexity |
| Temporary endpoint quantum workspace | $`O(n)`$ qubits; none retained as a bypass |

The gate counts allow gates between arbitrary addressed spins. They do not assert a geometrically local depth bound or price routing in a particular device. Reliable classical storage, calibration acquisition, and physical endpoint execution time are separate resources.

## 5. A composable endpoint error budget

Let the ideal keyed encoder and decoder be $`\mathcal E`$ and $`\mathcal R`$, including their classical registers. If implemented versions satisfy

```math
\frac12\|\widetilde{\mathcal E}-\mathcal E\|_\diamond\le\epsilon_E,
\qquad
\frac12\|\widetilde{\mathcal R}-\mathcal R\|_\diamond\le\epsilon_R,
```

where $`\Phi_t`$ below means the physical storage channel tensored with the identity on the retained classical key, then channel contraction and the triangle inequality give

```math
\frac12\|\widetilde{\mathcal R}\Phi_t
       \widetilde{\mathcal E}-\mathrm{id}\|_\diamond
\le \epsilon_{\rm storage}+\epsilon_E+\epsilon_R.
\qquad\text{(R13)}
```

For circuits represented as compositions of CPTP elementary operations, including measurements with their classical outputs, it suffices to assign operation $`\ell`$ a half-diamond error $`\xi_\ell`$ and require $`\sum_\ell\xi_\ell\le\epsilon_E+\epsilon_R`$. This is a hybrid argument, not a stochastic independence assumption. If a physical implementation has memory across operations, the full-boundary bounds in (R13) are the required interface.

A single-qubit unitary approximation with operator-norm error $`\zeta`$ has channel half-diamond error at most $`\zeta`$. For an uncompiled gate count $`G_0`$, compile each arbitrary rotation to accuracy $`\epsilon_{\rm synth}/G_0`$. Dawson–Nielsen, [*The Solovay–Kitaev algorithm*, Theorem 1 and Sections 2–3](https://arxiv.org/html/quant-ph/0505030v2), supplies an explicit fixed-gate-set construction with total gate count bounded by

```math
O\left(G_0\log^{3.97}\frac{G_0}{\epsilon_{\rm synth}}\right),
\qquad
G_0=O\bigl(M^2+K\mathrm{poly}(m)4^m\bigr).
\qquad\text{(R14)}
```

Clifford gates can be retained exactly in a Clifford-plus-$`T`$ gate set. State preparation, measurement, physical gate errors, and any noise accumulated while executing the endpoints must be included in the remaining boundary budget. The ideal storage theorem itself does not suppress those errors.

If a preliminary calibration procedure supplies valid certificates with failure probability at most $`\beta`$, independent of the unknown logical payload, averaging over that procedure adds at most $`\beta`$ to (R13). A specified classical-key failure probability can be charged in the same way. These additions require an actual supplied failure guarantee; no calibration or classical-memory protocol is inferred from a bit count.

## 6. An explicit growing-rate alternative

The fixed Tanner family does not by itself give a uniform efficient construction when its target rate tends to one: its degree, local search, tables, and decoding threshold then change. A separate CSS Reed–Solomon construction gives a controlled polynomial implementation in the slightly shorter regime below.

Let $`\ell=\lceil\log_2(n+1)\rceil`$, and choose

```math
m=2\left\lceil\frac{\ell+2\log_2\ell+8}{2}\right\rceil,
\qquad s=k_m,\qquad Q=2^s.
\qquad\text{(R15)}
```

Use all $`s=k_m`$ inner logical qubits as one $`Q`$-dimensional symbol. For sufficiently large $`n`$, $`Q\ge K`$, while $`m=O(\log n)`$ and $`Q\le2^m=\mathrm{poly}(n)`$. For example,

```math
D_m\ge\frac{2^m}{(m+1)(m/2+1)}
```

already suffices to verify $`2^{k_m}\ge K`$ for the choice (R15) at large $`n`$. The compiler can check this exact integer inequality before construction. Taking $`s=k_m`$ retains the uniform factor $`\rho_m\lt 2`$ in (R1); choosing only $`s=\lceil\log_2K\rceil`$ would not automatically retain it.

Choose $`K`$ distinct evaluation points in $`\mathbb F_Q`$. For $`0\le r\lt K/2`$, ordinary Reed–Solomon evaluation codes with the same points satisfy

```math
\mathrm{RS}_r\subset\mathrm{RS}_{K-r}.
```

The CSS pair

```math
C_X=\mathrm{RS}_{K-r},\qquad
C_Z=\mathrm{RS}_r^{\perp}
```

therefore has parameters

```math
[[K,K-2r,d\ge r+1]]_Q.
\qquad\text{(R16)}
```

This follows directly from nesting, the CSS dimension formula, and the MDS distances of Reed–Solomon codes and their duals. It is an inherited coding construction. Grassl–Geiselmann–Beth, [*Quantum Reed–Solomon Codes*](https://arxiv.org/pdf/quant-ph/9910059), gives the finite-field CSS approach and encoder/syndrome circuitry. Equation (R16) uses the nested-code formulation so that no special self-duality condition on the chosen evaluation points is needed.

The code corrects $`\lfloor r/2\rfloor`$ arbitrary bad inner blocks. Standard classical Reed–Solomon syndrome decoding is applied separately to the two final CSS syndromes. A binary basis and its trace-dual basis identify field Weyl operators with ordinary $`s`$-qubit Paulis; the key still uses $`2Ks=O(n)`$ bits. No coherent implementation of a classical error-location algorithm is required.

Set $`r=2\lceil\beta K\rceil`$ with $`\beta\to0`$. The outer rate is at least $`1-4\beta-O(1/K)`$, and Markov's inequality gives

```math
\epsilon_{\rm storage}\le p/\beta.
\qquad\text{(R17)}
```

For a sequence $`t=t_n`$ satisfying

```math
h_n=\frac{n^2}{(1+\Gamma W^2t_n)\ell^3}\longrightarrow\infty,
```

take $`C=\Theta(h_n^{1/8})`$ and $`\beta=\Theta(h_n^{-1/4})`$. Powers of two within fixed factors give exact rational choices. Assume certified uncertainty $`\eta=O(1/n)`$. Equations (R5)–(R6), $`m=\Theta(\ell)`$, and $`\rho_m\lt 2`$ yield

```math
p=O(C^2/h_n),\qquad
\epsilon_{\rm storage}=O(h_n^{-1/2})\longrightarrow0.
\qquad\text{(R18)}
```

Also $`Cm=o(n)`$, $`K\to\infty`$, $`\beta K\to\infty`$, and

```math
\frac{(K-2r)k_m}{n}\longrightarrow1.
```

For fixed positive $`\Gamma,W`$, this is the stated regime $`t_n=o(n^2/\log^3 n)`$. The weaker restricted-generator block estimate would instead give a fourth logarithmic power; (R18) uses the singlet-trace refinement (R1).

Finite-field arithmetic, CSS check construction, and classical Reed–Solomon decoding are polynomial in $`n`$. A general binary stabilizer encoder uses $`O(n^2)`$ Clifford gates. The deliberately conservative inner synthesis bound is also polynomial, since $`4^m=O(n^2\ell^4)`$: together with (R14), it gives $`n^3\log^{O(1)}(n/\epsilon_{\rm synth})`$ endpoint gates. This suffices for an algorithmic resource statement without claiming a small circuit or a favorable hardware depth.

The general $`t_n=o(n^2)`$ existence theorem, the fixed-rate Tanner implementation, and this Reed–Solomon construction are distinct guarantees. The logarithmic loss here is an achieved construction bound, not a converse or an optimal lifetime.

[Operational model](model.md) · [Storage theorem](storage_theorem.md) · [Related work](../references/related_work.md) · [Bibliography](../references/references.bib)
