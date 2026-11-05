# A finite-size storage theorem

This note proves an achievable storage interval for the model in [model.md](model.md). It includes all integer roundings, arbitrary supplied coefficient lists, correlated residual errors, and an arbitrary entangled reference. The outer code used in this proof is existential. Computational implementations of the endpoints are a separate question.

The noise consists of two Hermitian collective jumps

```math
A_x=\sum_{j=1}^n g_jX_j,\qquad
A_z=\sum_{j=1}^n g_jZ_j,\qquad
\mathcal L_n
=\gamma_x\mathcal D[A_x]+\gamma_z\mathcal D[A_z],
\qquad \Gamma=\gamma_x+\gamma_z,
```

where $`g_j\in[1,2]`$, both rates are positive and fixed independently of $`n`$, and $`\mathcal D[A](X)=AXA-\{A^2,X\}/2`$. There are no operations during storage.

## 1. Finite-size theorem

Fix an even integer $`m\ge4`$, a real number $`C>1`$, and an integer $`n\ge2Cm`$. Define

```math
B=\left\lfloor\frac{n}{Cm}\right\rfloor,\qquad
D_m=\frac{1}{m/2+1}\binom{m}{m/2},\qquad
k_m=\lfloor\log_2D_m\rfloor,\qquad
\rho_m=\frac{D_m}{2^{k_m}}\in[1,2).
```

Split $`[1,2]`$ into $`B`$ intervals of width $`1/B`$. In interval $`\ell`$, let $`n_\ell`$ be the number of supplied coefficients. Form $`\lfloor n_\ell/m\rfloor`$ disjoint complete blocks of $`m`$ spins, leaving the remaining spins unused. Put

```math
K=\sum_{\ell=1}^B\left\lfloor\frac{n_\ell}{m}\right\rfloor,
\qquad N=Km,\qquad M=Kk_m.
```

Thus $`N`$ is the number of retained physical spins and $`M`$ is the number of logical qubits available after inner singlet encoding. For each complete block $`b`$, define

```math
\bar g_b=\frac1m\sum_{j\in b}g_j,\qquad
v_b=\sum_{j\in b}(g_j-\bar g_b)^2,\qquad
\mu_b=\Gamma\rho_m\frac{m}{m-1}v_b.
```

Choose an integer $`h\ge0`$ with $`2h\le M`$. Define the Pauli-ball volume and redundancy

```math
V(M,h)=\sum_{j=0}^{2h}3^j\binom{M}{j},\qquad
s=\left\lceil\log_2V(M,h)\right\rceil.
```

Assume $`s\le M-1`$, and put $`k=M-s`$.

**Theorem 1.** There is an endpoint encoding and recovery protocol storing $`k`$ logical qubits in the original $`n`$ spins such that, for every $`t\ge0`$,

```math
\begin{aligned}
\epsilon_{\mathrm{mem}}(n,t)
&=\frac12\left\|\mathcal M_{n,t}
                 -\mathrm{id}_{2^k}\right\|_\diamond\\
&\le
\min\left\{
1,\,
\frac{k_m}{h+1}
\sum_{b=1}^K\left(1-e^{-\mu_bt}\right)
\right\}\\
&\le
\min\left\{
1,\,
\frac{\Gamma\rho_m m^2M}{4(m-1)B^2(h+1)}\,t
\right\}.
\end{aligned}
```

The protocol uses $`2M`$ independent uniform classical key bits and no retained quantum auxiliary system. Its encoder and recovery can be chosen independently of $`t`$. The bound therefore holds for the same protocol throughout any specified storage interval. Its rate obeys

```math
\frac{k}{n}
\ge
\frac{k_m}{m}\left(1-\frac{B(m-1)}n\right)
-\frac{\lceil\log_2V(M,h)\rceil}{n}.
```

Unused spins remain included in the denominator $`n`$. No spacing or probability assumption on the coefficients appears in this theorem.

Sections 2–7 give the proof. First, an exact local diamond-norm estimate controls every inner input. A sharper entanglement-infidelity estimate then supplies the quantity needed by Pauli twirling and outer recovery. These two error criteria are kept distinct.

## 2. Binning and the singlet code

### Exact binning loss

Take

```math
I_\ell=
\left[1+\frac{\ell-1}{B},\,1+\frac{\ell}{B}\right)
\quad(1\le\ell\lt B),
\qquad
I_B=\left[2-\frac1B,\,2\right].
```

Every discarded remainder is at most $`m-1`$. Consequently,

```math
N=n-\sum_{\ell=1}^B(n_\ell\bmod m)
\ge n-B(m-1)
\ge\left(1-\frac1C\right)n.
```

The final inequality uses $`B\le n/(Cm)`$. Since $`n/(Cm)\ge2`$,

```math
\frac{n}{2Cm}\le B\le\frac{n}{Cm}.
```

Let $`c_b`$ be the midpoint of the bin containing block $`b`$. Then $`|g_j-c_b|\le1/(2B)`$ for every spin in that block. The sample mean minimizes squared deviations, so

```math
v_b
=\min_{c\in\mathbb R}\sum_{j\in b}(g_j-c)^2
\le\sum_{j\in b}(g_j-c_b)^2
\le\frac{m}{4B^2}.
```

It follows that

```math
\mu_b\le\mu_{\max}
:=\frac{\Gamma\rho_m m^2}{4(m-1)B^2}
\le\frac{\Gamma\rho_m C^2m^4}{(m-1)n^2}.
```

Grouping is by supplied coefficient values. Spins in the same block need not be adjacent in physical space; joint endpoint operations are permitted.

### Singlet multiplicity and logical dimension

For $`m`$ spins, let $`P_m`$ project onto the full total-spin-zero subspace. Its dimension is

```math
\mathrm{rank}P_m
=\binom{m}{m/2}-\binom{m}{m/2+1}
=D_m.
```

To see the first equality, count states of magnetic quantum number zero and one. Each integer-spin irreducible representation with spin at least one contributes one state to both counts. A spin-zero representation contributes only to the first. Their difference is the singlet multiplicity.

Choose any fixed isometry

```math
E_b:\mathbb C^{2^{k_m}}\longrightarrow P_m\mathcal H_b,
\qquad Q_b=E_bE_b^\dagger\le P_m,
\qquad
\mathrm{Enc}_b(X)=E_bXE_b^\dagger.
```

No optimization over this subspace is required. The factor $`\rho_m\lt 2`$ accounts for using a power-of-two logical dimension within the full singlet sector.

For each Pauli axis $`\alpha`$, the collective operator $`J_{\alpha,b}=\sum_{j\in b}\sigma_{\alpha,j}`$ annihilates that sector, and every collective rotation acts there as identity. This is the standard noiseless-code mechanism for exactly collective noise; see [Zanardi and Rasetti (1997)](https://arxiv.org/abs/quant-ph/9705044).

The inner rate tends to one. The largest binomial coefficient is at least the average, giving the elementary bounds

```math
D_m\ge\frac{2^m}{(m+1)(m/2+1)},\qquad
k_m\ge
m-\log_2(m+1)-\log_2(m/2+1)-1.
```

Thus $`k_m/m\to1`$ along even $`m`$. The sharper asymptotic $`\log_2D_m=m-\tfrac32\log_2m+O(1)`$ is not needed for the proof.

## 3. Exact local diamond-norm estimate

On block $`b`$, write

```math
A_{\alpha,b}=c_bJ_{\alpha,b}+D_{\alpha,b},\qquad
D_{\alpha,b}
=\sum_{j\in b}(g_j-c_b)\sigma_{\alpha,j},\qquad
d_b=\sum_{j\in b}|g_j-c_b|.
```

All terms have the same Pauli axis. Hence

```math
[J_{\alpha,b},D_{\alpha,b}]=0,\qquad
J_{\alpha,b}P_m=0,
```

and, exactly,

```math
A_{\alpha,b}P_m=D_{\alpha,b}P_m,\qquad
A_{\alpha,b}^2P_m=D_{\alpha,b}^2P_m.
```

For any trace-class logical input operator $`X`$, including an arbitrary reference, the jump term is bounded by $`\|D_{\alpha,b}E_b\|^2\|X\|_1`$. Each anticommutator term, including its factor $`1/2`$, is bounded by $`\tfrac12\|D_{\alpha,b}^2E_b\|\|X\|_1`$. These follow directly from $`\|LXR\|_1\le\|L\|\|R\|\|X\|_1`$; reference identities do not alter the operator norms. Since $`\|D_{\alpha,b}\|\le d_b`$,

```math
\left\|\mathcal D[A_{\alpha,b}]
        \circ\mathrm{Enc}_b\right\|_\diamond
\le2d_b^2.
```

Let $`\mathcal L_b=\sum_\alpha\gamma_\alpha\mathcal D[A_{\alpha,b}]`$ and $`\Phi_{b,t}=e^{t\mathcal L_b}`$. Duhamel's identity gives

```math
(\Phi_{b,t}-\mathrm{id})\circ\mathrm{Enc}_b
=\int_0^t e^{u\mathcal L_b}
       \circ\mathcal L_b\circ\mathrm{Enc}_b\,du.
```

Each $`e^{u\mathcal L_b}`$ is a channel and has diamond norm one. Therefore,

```math
\frac12\left\|
\Phi_{b,t}\circ\mathrm{Enc}_b-\mathrm{Enc}_b
\right\|_\diamond
\le\min\{1,\Gamma t d_b^2\}.
```

This holds for every time and every reference-entangled input. It is not a short-time expansion. The absence of a term linear in the mismatch follows from the exact commutation and singlet-annihilation identities.

Choose a fixed logical state $`\tau_b`$ and the final inner decoder

```math
\mathrm{Dec}_b(Y)
=E_b^\dagger YE_b+
 \mathrm{Tr}[(I-Q_b)Y]\tau_b.
```

This channel is trace preserving, is a left inverse of $`\mathrm{Enc}_b`$, and replaces leakage by a fixed logical state. Contraction under the decoder preserves the bound above. The next section gives a stronger bound for the particular fidelity used by outer coding.

## 4. Sharper marginal entanglement-infidelity bound

Let $`d=2^{k_m}`$ and define the encoded maximally entangled state

```math
|\Omega_b\rangle
=\frac1{\sqrt d}\sum_{a=1}^d E_b|a\rangle\otimes|a\rangle,
\qquad
\omega_b=|\Omega_b\rangle\langle\Omega_b|.
```

Its physical survival probability is

```math
F_{\mathrm{surv},b}(t)
=\left\langle\omega_b,\,
(\Phi_{b,t}\otimes\mathrm{id})(\omega_b)
\right\rangle_{\mathrm{HS}}.
```

### Finite-time survival from the initial variance

For Hermitian $`A`$,

```math
\langle Y,\mathcal D[A](Y)\rangle_{\mathrm{HS}}
=-\frac12\|[A,Y]\|_2^2.
```

Thus $`\mathcal L_b\otimes\mathrm{id}`$ is self-adjoint and negative semidefinite on Hilbert–Schmidt operator space. As $`\|\omega_b\|_2^2=1`$, its spectral decomposition gives nonnegative $`w_\ell`$ summing to one and $`\lambda_\ell\ge0`$ such that

```math
F_{\mathrm{surv},b}(t)
=\sum_\ell w_\ell e^{-\lambda_\ell t}
\ge \exp\!\left[-t\sum_\ell w_\ell\lambda_\ell\right].
```

The last step is Jensen's inequality. The initial mean loss rate is

```math
\begin{aligned}
\sum_\ell w_\ell\lambda_\ell
&=-\langle\omega_b,
(\mathcal L_b\otimes\mathrm{id})(\omega_b)\rangle\\
&=\sum_\alpha\gamma_\alpha
\left[
\frac{\mathrm{Tr}(Q_bA_{\alpha,b}^2)}d
-\left|\frac{\mathrm{Tr}(Q_bA_{\alpha,b})}d\right|^2
\right].
\end{aligned}
```

A collective $`\pi`$ rotation about an axis perpendicular to $`\alpha`$ fixes every singlet vector and changes the sign of $`A_{\alpha,b}`$. Consequently $`P_mA_{\alpha,b}P_m=0`$, and the squared mean in this expression vanishes.

### Evaluating the full-singlet average

This established singlet moment also follows from the reduced states in [Urizar-Lanz et al. (2013), Eqs. (10), (16)–(18)](https://www.gtoth.eu/Publications/PRA13_singlet.pdf).

The full projector $`P_m`$ is invariant under permutations. The value of $`\mathrm{Tr}(P_m\sigma_{\alpha,i}\sigma_{\alpha,j})/D_m`$ is therefore the same for every distinct pair. Taking the trace of $`J_{\alpha,b}^2P_m=0`$ gives

```math
\frac{\mathrm{Tr}
(P_m\sigma_{\alpha,i}\sigma_{\alpha,j})}{D_m}
=-\frac1{m-1}\qquad(i\ne j).
```

Expanding the weighted square yields

```math
\begin{aligned}
\frac{\mathrm{Tr}(P_mA_{\alpha,b}^2)}{D_m}
&=\sum_jg_j^2-\frac1{m-1}\sum_{i\ne j}g_ig_j\\
&=\frac{m}{m-1}
  \sum_{j\in b}(g_j-\bar g_b)^2.
\end{aligned}
```

Since $`Q_b\le P_m`$ and $`A_{\alpha,b}^2`$ is positive,

```math
\frac{\mathrm{Tr}(Q_bA_{\alpha,b}^2)}d
\le\rho_m
\frac{\mathrm{Tr}(P_mA_{\alpha,b}^2)}{D_m}.
```

Summing the axes proves $`F_{\mathrm{surv},b}(t)\ge e^{-\mu_bt}`$.

### Passing to the logical channel

Let $`\mathcal N_b=\mathrm{Dec}_b\circ\Phi_{b,t}\circ\mathrm{Enc}_b`$, and let $`F_{e,b}`$ be its entanglement fidelity for the maximally mixed logical input. The decoder has a Kraus operator $`E_b^\dagger`$. Its contribution to that fidelity is exactly the physical survival probability; the leakage-replacement Kraus operators add nonnegative terms. Hence

```math
p_b:=1-F_{e,b}
\le1-e^{-\mu_bt}
\le\mu_bt.
```

This is an entanglement-infidelity estimate. It is not asserted to be a local diamond-norm estimate. Section 6 explains how it becomes an exact marginal error-probability bound after Pauli twirling.

## 5. Exact non-signalling and unused spins

For any physical subset $`S`$ and its complement $`T`$, write

```math
A_\alpha=A_{\alpha,S}\otimes I_T+
         I_S\otimes A_{\alpha,T}.
```

For every operator $`Y`$, including one correlated with a reference,

```math
\mathrm{Tr}_T
[I_S\otimes A_{\alpha,T},Y]=0.
```

Using $`\mathcal D[A](Y)=-[A,[A,Y]]/2`$, expand the double commutator. The terms containing one or two commutators with $`A_{\alpha,T}`$ vanish under the partial trace, leaving

```math
\mathrm{Tr}_T\mathcal D[A_\alpha](Y)
=\mathcal D[A_{\alpha,S}](\mathrm{Tr}_TY).
```

Summing over axes and exponentiating this intertwining identity gives

```math
\mathrm{Tr}_T\circ\Phi_{n,t}
=\Phi_{S,t}\circ\mathrm{Tr}_T.
```

The marginal channel on a block is therefore exactly its local collective semigroup, regardless of the other input blocks. This does not assert independence of their noise. It also justifies initializing the unused spins in a fixed state and tracing them out at recovery.

The product inner encoder and decoder define a channel on the $`M`$ inner logical qubits. Here $`\Phi_{N,t}`$ denotes the channel on the actual retained subset, after relabelling those spins:

```math
\mathcal N
=\left(\bigotimes_b\mathrm{Dec}_b\right)
 \circ\Phi_{N,t}
 \circ\left(\bigotimes_b\mathrm{Enc}_b\right).
```

Trace preservation of the other endpoint maps implies the exact marginal property

```math
\mathrm{Tr}_{\ne b}\circ\mathcal N
=\mathcal N_b\circ\mathrm{Tr}_{\ne b}.
```

## 6. Global Pauli twirling and correlated-error correction

Let $`\mathcal P_M`$ be the $`4^M`$ tensor-product Pauli operators modulo phase. Choose uniform $`P\in\mathcal P_M`$, apply it after the outer encoder and before the inner encoders, and undo it after the inner decoders. This is equivalent to independent uniform Pauli keys on the inner blocks. The averaged channel is

```math
\mathcal T(\mathcal N)(X)
=4^{-M}\sum_{P\in\mathcal P_M}
P^\dagger\mathcal N(PXP^\dagger)P.
```

### A global Pauli distribution, with all correlations retained

Expand every Kraus operator of $`\mathcal N`$ as $`K_a=\sum_Q c_{aQ}Q`$. Pauli conjugation multiplies each coefficient by its commutation character. Averaging the characters kills the cross terms between distinct $`Q`$ and $`Q'`$. Therefore

```math
\mathcal T(\mathcal N)(X)
=\sum_{Q\in\mathcal P_M}q_QQXQ^\dagger,\qquad
q_Q=\sum_a|c_{aQ}|^2\ge0,\qquad
\sum_Qq_Q=1.
```

The last identity follows from trace preservation and orthogonality of the Pauli basis. This distribution can have arbitrary correlations among blocks.

The marginal property in Section 5 implies that the distribution of the Pauli factor on block $`b`$ is the twirl of $`\mathcal N_b`$. For a Pauli channel, entanglement fidelity equals the identity-Pauli probability, because all other Pauli operators have zero trace. Entanglement fidelity is unchanged by twirling, as is also immediate from $`F_e(\mathcal N_b)=d^{-2}\sum_a|\mathrm{Tr}K_a|^2`$. Consequently,

```math
\Pr(Q|_b\ne I)=p_b\le1-e^{-\mu_bt}.
```

### The outer threshold counts logical qubits

Write $`\mathrm{wt}(Q)`$ for the number of nonidentity single-qubit factors in $`Q`$. A nonidentity inner block can contain as many as $`k_m`$ such factors. Thus

```math
\mathbb E[\mathrm{wt}(Q)]
\le k_m\sum_b\Pr(Q|_b\ne I)
\le k_m\sum_b(1-e^{-\mu_bt}).
```

The factor $`k_m`$ is essential: block-error count and qubit-error weight are different quantities for this outer code.

Choose an outer code correcting every Pauli error of weight at most $`h`$. Integer-valued Markov gives

```math
p_{\mathrm{bad}}
:=\Pr(\mathrm{wt}(Q)>h)
\le\frac{\mathbb E[\mathrm{wt}(Q)]}{h+1}.
```

Every Pauli in the complementary event is corrected exactly, for all reference-entangled inputs. The recovered channel has the form

```math
\mathcal M_{n,t}
=(1-p_{\mathrm{bad}})\mathrm{id}
+p_{\mathrm{bad}}\mathcal B
```

for a channel $`\mathcal B`$. The half-diamond distance between any two channels is at most one, so

```math
\epsilon_{\mathrm{mem}}(n,t)
\le p_{\mathrm{bad}}
\le\frac{k_m}{h+1}\sum_b(1-e^{-\mu_bt}).
```

Together with $`\mu_b\le\mu_{\max}`$, this is the error bound of Theorem 1. No independence assumption, concentration estimate, or short-time approximation is used.

## 7. Finite Gilbert–Varshamov outer code

Here is the exact counting argument for the chosen redundancy. The underlying binary stabilizer formalism is standard; see [Gottesman, *Stabilizer Codes and Quantum Error Correction* (1997)](https://arxiv.org/abs/quant-ph/9705052). Perfect recovery of the resulting error set follows from [Knill and Laflamme's quantum error-correction conditions (1997)](https://doi.org/10.1103/PhysRevA.55.900).

Represent Paulis modulo phase by $`\mathbb F_2^{2M}`$. Choose uniformly a totally isotropic subspace $`S`$ of dimension $`s`$. It defines a stabilizer code of dimension $`2^{M-s}`$; its Pauli normalizer is $`S^\perp`$, of dimension $`2M-s`$.

The symplectic group is transitive on nonzero vectors. For every fixed nonzero $`v`$,

```math
\Pr(v\in S^\perp)
=\frac{2^{2M-s}-1}{2^{2M}-1}.
```

There are $`V(M,h)-1`$ nonzero Paulis of weight at most $`2h`$. If $`s>0`$, union bound gives

```math
\begin{aligned}
\Pr\bigl(\exists\,v\in S^\perp\setminus\{0\}:
             \mathrm{wt}(v)\le2h\bigr)
&\le
(V(M,h)-1)\frac{2^{2M-s}-1}{2^{2M}-1}\\
&\lt (V(M,h)-1)2^{-s}\\
&\le\frac{V(M,h)-1}{V(M,h)}\lt 1.
\end{aligned}
```

Some stabilizer therefore has no such vector. Its distance is at least $`2h+1`$. Products of two Pauli errors of weight at most $`h`$ have weight at most $`2h`$, so that code corrects the entire required error set.

If $`s=0`$, then $`V(M,h)=1`$ and $`h=0`$; the full $`M`$-qubit space works. The hypothesis $`s\le M-1`$ guarantees at least one logical qubit.

This is an existence proof, with no efficient search for the stabilizer or efficient decoder implied. Combined with Sections 2–6, it completes the proof of Theorem 1.

## 8. Explicit asymptotic consequences

### 8.1 Every fixed rate below one permits a quadratic interval

Define, with the entropy endpoints interpreted by continuity,

```math
H_2(x)=-x\log_2x-(1-x)\log_2(1-x),\qquad
f(q)=H_2(2q)+2q\log_2 3.
```

Fix $`0\lt R\lt 1`$ and $`0\lt \epsilon\lt 1`$. Choose fixed even $`m\ge4`$, $`C>1`$, and $`q\in(0,1/4)`$ such that

```math
a:=\left(1-\frac1C\right)\frac{k_m}{m},\qquad
\sigma:=a[1-f(q)]-R>0.
```

Such constants exist because $`k_m/m\to1`$, $`1-1/C\to1`$, and $`f(q)\to0`$ as $`q\downarrow0`$. Once chosen, they do not vary with $`n`$. Set

```math
h=\lfloor qM\rfloor,\qquad
n_0=\left\lceil\max\left\{2Cm,\frac1\sigma\right\}\right\rceil,
\qquad
c_{R,\epsilon}
=\frac{\epsilon q(m-1)}
       {\Gamma\rho_m C^2m^4}.
```

Then every $`n\ge n_0`$ and every coefficient list in $`[1,2]^n`$ admit storage of at least $`Rn`$ logical qubits with

```math
\epsilon_{\mathrm{mem}}(n,t)\le\epsilon
\qquad\text{for all}\qquad
0\le t\le c_{R,\epsilon}n^2.
```

For the rate proof, put $`r=2h\le2qM\lt M/2`$. The binomial-volume estimate and $`3^j\le3^r`$ imply

```math
\sum_{j=0}^r\binom Mj\le2^{MH_2(r/M)},\qquad
V(M,h)\le2^{Mf(q)},\qquad
s\le Mf(q)+1.
```

Thus, with all rounding terms included,

```math
k=M-s
\ge M[1-f(q)]-1
\ge an[1-f(q)]-1
\ge Rn.
```

In particular $`k\ge1`$, verifying Theorem 1's redundancy condition. For the error, $`h+1>qM`$, so

```math
\epsilon_{\mathrm{mem}}(n,t)
\le\frac{\mu_{\max}t}{q}
\le
\frac{\Gamma\rho_m C^2m^4}{(m-1)q}\frac{t}{n^2}.
```

This proves the claimed constant. It is conservative and may deteriorate considerably as the target rate approaches one.

### 8.2 Rate one for every subquadratic time sequence

Let $`t_n\ge0`$ with $`t_n=o(n^2)`$. For sufficiently large $`n`$, define

```math
r_n=\frac{n^2}{1+t_n},\qquad
u_n=\min\{r_n^{1/12},\ln n\},\qquad
C_n=u_n,\qquad
m_n=2\left\lfloor\frac{u_n}{2}\right\rfloor,\qquad
q_n=\frac1{u_n}.
```

Both $`r_n`$ and $`u_n`$ diverge. Eventually $`m_n\ge4`$, $`q_n\lt 1/4`$, $`f(q_n)\lt 1`$, and $`n\ge2C_nm_n`$. Use $`h_n=\lfloor q_nM_n\rfloor`$ and the finite construction. Its rate satisfies

```math
\frac{k_n}{n}
\ge
\left(1-\frac1{u_n}\right)
\frac{k_{m_n}}{m_n}
[1-f(1/u_n)]-\frac1n
\longrightarrow1.
```

This lower bound is positive for sufficiently large $`n`$, verifying the finite theorem's condition $`s\le M_n-1`$.

For $`m\ge4`$, $`\rho_m m^4/(m-1)\le(8/3)m^3`$. Since $`m_n\le u_n`$,

```math
\begin{aligned}
\epsilon_{\mathrm{mem}}(n,t_n)
&\le\frac83\Gamma
\frac{C_n^2m_n^3}{q_n}\frac{t_n}{n^2}\\
&\le\frac83\Gamma\frac{u_n^6}{r_n}\\
&\le\frac83\Gamma r_n^{-1/2}
\longrightarrow0.
\end{aligned}
```

The same code works throughout $`0\le t\le t_n`$. The exponent $`1/12`$ is a convenient choice with slack, not an optimized tradeoff. This rate-one statement uses the existential Gilbert–Varshamov decoder.

### 8.3 A deterministic profile and the variance constant

For $`g_j=1+j/n`$, use consecutive blocks of even size $`m`$ and suppose for simplicity that $`m`$ divides $`n`$. No binning loss is needed. One block has exactly

```math
v_b=\frac{m(m^2-1)}{12n^2},\qquad
\mu_b=\frac{\Gamma\rho_m m^2(m+1)}{12n^2}.
```

For $`m=4`$, $`D_m=2`$ and $`\rho_m=1`$. With $`\gamma_x=\gamma_z=1`$,

```math
p_b\le1-\exp\!\left[-\frac{40t}{3n^2}\right]
\le\frac{40t}{3n^2}.
```

The same outer-code proof then applies. This example exhibits the achievable scale without a calibration or random-spacing assumption. It is not a lifetime converse.

## 9. Deterministic existence for a prescribed time

The randomized construction also gives a deterministic existence statement. This section fixes one prescribed duration $`t`$. The key and subspace found here may depend on that duration. The argument does not give one deterministic code uniform over an entire time interval.

Suppose the averaged recovered channel on $`D=2^k`$ dimensions obeys

```math
\frac12\|\mathbb E_\kappa\mathcal M_\kappa
                 -\mathrm{id}_D\|_\diamond\le\epsilon,
\qquad 0\le\epsilon\lt 1.
```

Its entanglement fidelity is at least $`1-\epsilon`$. That fidelity is linear in the channel, so some fixed key gives a channel $`\mathcal M`$ with $`F_e(\mathcal M)\ge1-\epsilon`$.

A unitary change of Kraus basis arranges its Kraus operators to satisfy

```math
\mathrm{Tr}K_0=D\sqrt{F_e(\mathcal M)}
\quad\text{real and nonnegative},\qquad
\mathrm{Tr}K_a=0\quad(a>0).
```

Define isometries

```math
V=\sum_aK_a\otimes|a\rangle,\qquad
W=I_D\otimes|0\rangle.
```

They satisfy

```math
T:=(V-W)^\dagger(V-W)
=2I_D-K_0-K_0^\dagger\ge0,
\qquad
\frac{\mathrm{Tr}T}{D}
=2(1-\sqrt{F_e(\mathcal M)})\le2\epsilon.
```

At least $`D/2`$ eigenvectors of $`T`$ have eigenvalue at most $`4\epsilon`$. Choose an isometry $`F:\mathbb C^{D/2}\to\mathbb C^D`$ into their span. Then

```math
\|(V-W)F\|\le2\sqrt\epsilon.
```

For any input entangled with a reference, the resulting two purifications differ in norm by at most this amount. Their half trace distance, and that of their partial traces, is bounded by the same amount. Therefore,

```math
\frac12\|\mathcal M\circ\mathrm{Enc}_F
                 -\mathrm{Enc}_F\|_\diamond
\le\min\{1,2\sqrt\epsilon\}.
```

Following the original recovery by a trace-preserving left inverse of $`\mathrm{Enc}_F`$ gives a deterministic logical channel on $`k-1`$ qubits with this error. For $`\epsilon=0`$, $`T=0`$ and no restriction is necessary.

The loss of at most one logical qubit leaves the asymptotic rates unchanged. To obtain deterministic target error $`\epsilon_{\mathrm{det}}`$, use randomized error at most $`\epsilon_{\mathrm{det}}^2/4`$ and allow one qubit of rate slack. The fixed-rate quadratic scale and rate-one subquadratic limit therefore remain valid as deterministic existence statements for prescribed durations. No efficient procedure for finding or implementing $`F`$ is established.

## 10. Interpretation and inherited ingredients

The theorem is a finite-time guarantee after endpoint recovery. It does not assert that the raw physical code state remains near its initial state throughout the quadratic interval. It also does not replace the common-field channel by independent residual block noise.

Exact singlet encoding, stabilizer error correction, Pauli twirling, and concatenation are established ingredients. In particular, [Lidar, Bacon, and Whaley (1999)](https://arxiv.org/abs/quant-ph/9809081) already combine decoherence-free inner blocks with outer error correction and handle leakage. The derivation above supplies bounded-coefficient grouping, an exact marginal identity, and a size–rate–time guarantee under the actual correlated noncommuting channel.

For generic distinct coefficients the associative interaction algebra is full, as [symmetry.md](symmetry.md) proves. That is compatible with approximate recovery over a size-dependent interval.

The achieved scale is not an upper bound on the best possible lifetime. All constants keep the noise rates and coefficient range fixed. Supplied calibration, ideal endpoint operations, and reliable classical key storage are assumptions of the constructive protocol. Deterministic expurgation removes the retained key at the stated cost, without an efficiency guarantee.
