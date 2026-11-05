# How a mismatched spin register stores quantum information

Imagine placing an unknown quantum state in a collection of spins, leaving the collection alone, and asking for the state back later. The state may be entangled with a distant system that the memory never touches. A successful recovery must preserve that entanglement too.

The spins in this project experience the same two fluctuating fields, but each spin couples with a different strength. Exact collective protection is then generally absent. The result concerns what can still be recovered at a finite time: grouping spins with nearby coupling strengths, encoding into their singlet sectors, and correcting the remaining correlated errors at the endpoint gives a storage interval that grows with register size.

This tutorial follows the settled [30-milestone map](milestones.md) in eight connected steps. Its sole educational anchor is **Nielsen and Chuang, _Quantum Computation and Quantum Information_, 10th Anniversary Edition**. The [anchor bridge](anchor_bridge.md) gives the verified edition, section pointers, notation and research-level additions. The linked scientific pages contain the exact statements and proofs.

## 1. What must survive? — M01–M04

A physical spin has a two-dimensional state space. The Pauli operators $`X,Y,Z`$ describe three axes and have eigenvalues $`+1`$ and $`-1`$. Their noncommutation matters: protecting against rotations about one axis does not automatically protect against a second axis.

Several spins have a tensor-product state space. A logical qubit can occupy a two-dimensional subspace spread across several of them. Its information need not appear in any individual spin. For example, the entangled state

```math
|\Phi\rangle_{LR}
=\frac{|0\rangle_L|0\rangle_R+|1\rangle_L|1\rangle_R}{\sqrt2}
```

has a maximally mixed reduced state on the logical system $`L`$. A device that outputs a maximally mixed state regardless of its input would reproduce that marginal while destroying the joint state with the reference $`R`$. Checking only the marginal would miss the failure.

Density operators and partial traces let us keep these two descriptions separate. The partial trace gives a subsystem's state; it does not assert that the full state is a product. A channel describes a physical transformation, including noise, encoding and recovery. In a Kraus representation,

```math
\mathcal N(\rho)=\sum_a K_a\rho K_a^\dagger,
\qquad \sum_a K_a^\dagger K_a=I.
```

The second identity makes the channel trace preserving. The Kraus label is a mathematical description of possible environment effects; the memory protocol need not observe it. These foundations enter the [operational model](../science/model.md) through a composition of an encoder, a storage channel and a recovery.

## 2. Shared noise and the right error criterion — M05–M08

Let $`n`$ be the number of physical spins, with supplied coefficients $`g_j\in[1,2]`$. The main model has two Hermitian collective jumps:

```math
\begin{gathered}
A_x=\sum_{j=1}^n g_jX_j,
\qquad A_z=\sum_{j=1}^n g_jZ_j,\\
\mathcal L_n=\gamma_x\mathcal D[A_x]+\gamma_z\mathcal D[A_z],\\
\mathcal D[A](\rho)=A\rho A-\frac12\{A^2,\rho\},
\qquad \Phi_{n,t}=e^{t\mathcal L_n}.
\end{gathered}
```

The positive rates $`\gamma_x,\gamma_z`$ stay fixed as $`n`$ grows. There is no additional Hamiltonian, and the collective jumps are not divided by register size. Write $`\Gamma=\gamma_x+\gamma_z`$.

One can realize this channel by applying a product of one-spin unitaries driven by the same two Brownian field paths. Conditional on the paths, every spin rotates locally. Averaging over the shared paths creates a correlated channel. Replacing it by a product of independently averaged one-spin channels would discard the physical resource that the code uses. [Model Section 2](../science/model.md#2-what-the-common-field-assumption-means) gives the precise stochastic representation.

Two different performance quantities will be needed. A block's entanglement fidelity is its decoded overlap with a maximally entangled input and reference. If $`\omega`$ is that normalized Bell-state density operator,

```math
F_e(\mathcal N)
=\operatorname{Tr}\!\left[
\omega(\mathcal N\otimes\operatorname{id})(\omega)
\right].
```

This is an overlap. Under the root state-fidelity convention, the corresponding state fidelity is $`\sqrt{F_e}`$. The quantity bounded locally will be $`p=1-F_e`$.

The final memory criterion is stronger in its quantifiers. If $`\mathcal M`$ is the recovered logical channel, define

```math
\epsilon_{\mathrm{mem}}
=\frac12\|\mathcal M-\operatorname{id}\|_\diamond.
```

For a difference of channels, this is the largest output trace distance from the ideal state, allowing every input entangled with a reference. Trace distance here means one half of the trace norm of the difference. The [bridge's explicit definition](anchor_bridge.md#fidelity-and-complete-channel-error) supplies the reference formulation. A local Bell-overlap bound will reach this final criterion through twirling and exact error correction; we will not identify the two quantities directly.

## 3. Encode a subspace, then recover it — M09–M12

An inner encoder is an isometry $`E_b`$ from logical states into a physical block $`b`$. Its image projector is $`Q_b=E_bE_b^\dagger`$. Noise can carry a state outside that image, which is called leakage. A complete decoder must say what happens to those outcomes. The decoder used here is

```math
\operatorname{Dec}_b(Y)
=E_b^\dagger YE_b
+\operatorname{Tr}[(I-Q_b)Y]\tau_b,
```

where $`\tau_b`$ is a fixed logical state. It recovers the encoded component and replaces leakage. This map is trace preserving; no favorable outcome is postselected.

The useful subspace is the total-spin-zero, or singlet, sector. Every equal rotation of all spins in a block acts as identity there. Equivalently,

```math
J_{\alpha,b}P_m=0,
\qquad J_{\alpha,b}=\sum_{j\in b}\sigma_{\alpha,j},
```

where $`P_m`$ projects onto the full singlet sector of an even number $`m`$ of spins. Two spins have only one singlet state. A one-dimensional space cannot hold an unknown qubit. Four spins have a two-dimensional singlet sector and can hold one.

The second encoding layer is an outer quantum code acting on the logical outputs of many inner blocks. Stabilizer checks are commuting Pauli observables whose common positive eigenspace defines the code; their measured signs form an error syndrome. Code distance at least $`2h+1`$ ensures correction of every Pauli error on at most $`h`$ positions, because a product of two such errors has weight at most $`2h`$ and cannot implement an undetectable nontrivial logical operation. This error-set guarantee holds for any probability distribution. Independence is not required, which lets us use a code under shared-field noise.

The complete storage task now has a clear interface. Joint encoding happens before storage, joint recovery after it. There are no controls, measurements or resets during storage, and no retained quantum auxiliary system carrying part of the input. The constructive protocol retains an input-independent classical Pauli key. Unused spins still count in the physical rate denominator. These are the assumptions of the [memory model](../science/model.md#3-permitted-operations-and-the-error-criterion), rather than implementation details that can be omitted from its rate claim.

## 4. Turn coefficient proximity into a finite-time bound — M13–M17

There is no promise that the supplied coefficients are random or regularly spaced. Partitioning their fixed interval nevertheless produces many narrow groups. Choose even $`m\ge4`$ and $`C>1`$ with $`n\ge2Cm`$, and use

```math
B=\left\lfloor\frac{n}{Cm}\right\rfloor
```

bins. Form complete groups of $`m`$ spins within each bin. Each bin loses at most $`m-1`$ leftover spins, so the total retained number $`N`$ obeys

```math
N\ge n-B(m-1)\ge(1-1/C)n.
```

Grouping uses coefficient values; it can join physically separated spins because joint endpoint operations are permitted. More spins in the same bounded coefficient interval supply finer resolution without reducing the physical noise rates.

The singlet dimension and the number of encoded qubits per block are

```math
\begin{gathered}
D_m=\frac{1}{m/2+1}\binom m{m/2},
\qquad k_m=\lfloor\log_2D_m\rfloor,\\
\rho_m=\frac{D_m}{2^{k_m}}\in[1,2).
\end{gathered}
```

We select a $`2^{k_m}`$-dimensional subspace inside the full sector. The factor $`\rho_m`$ pays for that restriction in an average-noise estimate. As the even block size grows, $`k_m/m`$ approaches one. [Theorem Section 2](../science/storage_theorem.md#2-binning-and-the-singlet-code) derives the count and all rounding losses.

Two bounds explain why a narrow block helps. First, split its same-axis jump into an exactly collective term and a mismatch term. The collective term annihilates the singlet sector and commutes with that same-axis mismatch. Duhamel integration then gives an all-time local diamond bound proportional to time times the square of the sum of absolute coefficient mismatches. It does not require the noisy state to remain inside the code throughout storage. This is the [exact local argument](../science/storage_theorem.md#3-exact-local-diamond-norm-estimate).

The sharper bound used for the outer code measures coefficient variance. Put

```math
\begin{gathered}
\bar g_b=\frac1m\sum_{j\in b}g_j,
\qquad v_b=\sum_{j\in b}(g_j-\bar g_b)^2,\\
\mu_b=\Gamma\rho_m\frac{m}{m-1}v_b.
\end{gathered}
```

Permutation symmetry of the full singlet projector fixes each distinct pair's same-axis covariance to $`-1/(m-1)`$. Expanding the weighted jump's square therefore cancels the common component and leaves $`mv_b/(m-1)`$. Positivity controls the chosen logical subspace at the cost $`\rho_m`$. This singlet-moment structure is inherited and explicitly attributed in [the scientific proof](../science/storage_theorem.md#evaluating-the-full-singlet-average).

An initial loss rate alone would be insufficient to guarantee long storage. The additional step is spectral. For Hermitian jumps, the generator is self-adjoint and negative on Hilbert–Schmidt operator space. The encoded Bell state's survival is consequently a positive weighted sum of decaying exponentials. Jensen's inequality lower-bounds that survival by an exponential of its mean initial loss rate. The leakage decoder retains this contribution, giving

```math
p_b=1-F_{e,b}\le1-e^{-\mu_bt}\le\mu_bt.
```

This bound holds for every time. Since one bin has width $`1/B`$, its variance satisfies $`v_b\le m/(4B^2)`$. With fixed block and overhead parameters, $`\mu_b`$ therefore has a uniform $`O(n^{-2})`$ upper bound; it can vanish when all coefficients in a block coincide. The exponential argument and the reference-uniform local argument have different roles and error metrics; [Theorem Sections 3–4](../science/storage_theorem.md#3-exact-local-diamond-norm-estimate) keep them separate.

## 5. Recover despite correlations — M18–M22

The block calculation remains valid inside the full register. For a Hermitian collective jump split between a block and its complement, every commutator wholly on the traced-out complement has zero partial trace. Expanding the dissipator as a double commutator gives the exact identity

```math
\operatorname{Tr}_T\circ\Phi_{n,t}
=\Phi_{S,t}\circ\operatorname{Tr}_T.
```

Thus each block's marginal channel is the one just analyzed, even when its input is entangled with the other blocks. The global errors remain correlated. The same identity accounts for unused spectator spins. [Theorem Section 5](../science/storage_theorem.md#5-exact-non-signalling-and-unused-spins) proves the statement for arbitrary operators and references.

There are $`K`$ complete blocks and $`M=Kk_m`$ inner logical qubits. Choose a uniform tensor-product Pauli on those $`M`$ qubits, apply it before inner encoding, and undo it after inner decoding. Retain the $`2M`$ classical bits specifying that choice. Averaging this protocol eliminates off-diagonal terms in the channel's Pauli expansion, leaving a joint Pauli distribution. It does not remove correlations between positions. A block's probability of a nonidentity Pauli is exactly its entanglement infidelity $`p_b`$.

Let $`W`$ count the erroneous single-qubit Pauli positions. A bad inner block can affect up to $`k_m`$ positions, so

```math
\mathbb E W\le k_m\sum_b p_b.
```

If the outer code corrects weight at most $`h`$, failure can occur only when $`W\ge h+1`$. Integer-valued Markov gives

```math
\Pr(W>h)\le\frac{k_m}{h+1}\sum_b p_b.
```

On all successful branches, recovery is exactly the identity, including on an entangled reference. The entire recovered channel is an identity channel mixed with a failure channel. Its half-diamond error is therefore at most the failure probability:

```math
\epsilon_{\mathrm{mem}}(n,t)
\le\min\left\{1,
\frac{k_m}{h+1}\sum_b(1-e^{-\mu_bt})\right\}.
```

This is the central local-to-global step. It uses marginal expectations and an error-set guarantee, with no concentration or independence assumption. The guarantee averages over the independent classical key; it does not assert that every key performs equally well.

For the general finite theorem, a stabilizer counting argument supplies an outer code. With

```math
V(M,h)=\sum_{j=0}^{2h}3^j\binom Mj,
\qquad s=\lceil\log_2V(M,h)\rceil,
```

the conditions $`2h\le M`$ and $`s\le M-1`$ guarantee a code storing $`k=M-s`$ qubits and correcting weight $`h`$. The count is an existence proof. The [complete theorem](../science/storage_theorem.md#1-finite-size-theorem) specifies the integer hypotheses, physical rate, key and uniformity over time.

### A complete 20-spin example

Take $`n=20`$, $`g_j=1+j/20`$, and $`\gamma_x=\gamma_z=1`$. Form five consecutive blocks of four spins. There are no unused spins. Each block's two-dimensional singlet sector holds one inner logical qubit.

One explicit inner basis uses the two-spin states

```math
\begin{gathered}
|s\rangle=(|01\rangle-|10\rangle)/\sqrt2,\\
|t_+\rangle=|00\rangle,\quad
|t_-\rangle=|11\rangle,\quad
|t_0\rangle=(|01\rangle+|10\rangle)/\sqrt2.
\end{gathered}
```

Pair positions 1–2 and 3–4 within each block and encode as

```math
\begin{aligned}
|0_{\mathrm{in}}\rangle&=|s\rangle|s\rangle,\\
|1_{\mathrm{in}}\rangle
&=\frac{|t_+\rangle|t_-\rangle
+|t_-\rangle|t_+\rangle
-|t_0\rangle|t_0\rangle}{\sqrt3}.
\end{aligned}
```

These orthonormal states are both total-spin zero. Use the standard five-qubit outer code, whose stabilizer generators are

```math
XZZXI,\quad IXZZX,\quad XIXZZ,\quad ZXIXZ.
```

It encodes one unknown logical qubit into the five inner qubits and corrects any one-qubit Pauli error. This code and the exhaustive Pauli verification are described in [the outer-recovery example](../science/examples.md#5-outer-correction-under-an-explicitly-correlated-law).

The operations are now explicit. Encode the input with that outer code, choose one uniform Pauli for each of its five output qubits, and retain the ten key bits. Encode each resulting qubit into the displayed four-spin basis. Leave all 20 spins untouched during storage. At recovery, apply each trace-preserving inner decoder, undo the five keyed Paulis, measure the four outer stabilizers, apply the syndrome's one-qubit correction, and decode the outer code. The output is one recovered quantum qubit; syndrome measurements occur only at this endpoint.

For a four-spin consecutive block, the coefficient deviations from its mean are $`(-3,-1,1,3)/(2n)`$. Therefore

```math
v_b=\frac5{n^2},\qquad
\rho_4=1,\qquad
\mu_b=2\frac43\frac5{20^2}=\frac1{30}.
```

For every $`0\le t\le2/5`$,

```math
p_b\le1-e^{-1/75}\le\frac1{75}.
```

Here $`k_m=1`$ and the outer correction radius is $`h=1`$. Correlations can be arbitrary, yet

```math
\mathbb E W\le\frac5{75}=\frac1{15},
\qquad
\epsilon_{\mathrm{mem}}
\le\Pr(W\ge2)\le\frac1{30}.
```

The rate is $`1/20`$, and the same keyed encoding and recovery work throughout that interval. This deliberately small example exhibits the operations and error calculation; the large-size construction is what raises the rate. We used the known five-qubit code directly. The sufficient finite counting bound above does not certify that small code, so this is an instance of the general correlated-recovery argument, rather than of that sufficient counting condition. The numerical suite checks finite inner channels and all five-qubit Paulis separately; the 20-spin guarantee here is analytic.

## 6. What the size-dependent theorem says — M23–M25

Fix a target rate $`0<R<1`$ and target error $`0<\epsilon<1`$. Choose a sufficiently large but fixed even block size, a sufficiently small discarded fraction, and a sufficiently small fixed outer correction fraction. The finite estimates then give constants $`c_{R,\epsilon}>0`$ and $`n_0`$ such that every supplied list in $`[1,2]^n`$, for $`n\ge n_0`$, permits

```math
k\ge Rn,\qquad
\epsilon_{\mathrm{mem}}(n,t)\le\epsilon
\quad(0\le t\le c_{R,\epsilon}n^2).
```

The constant can become small when the requested rate approaches one or the error approaches zero. A separate parameter choice lets the block size and overhead controls grow slowly with $`n`$. For every time sequence $`t_n=o(n^2)`$, the theorem then achieves $`k_n/n\to1`$ and $`\epsilon_{\mathrm{mem}}(n,t_n)\to0`$. Its encoder and recovery also work throughout the shorter interval. [Theorem Section 8](../science/storage_theorem.md#8-explicit-asymptotic-consequences) proves both quantifier statements explicitly.

A deterministic existence statement can remove the retained key for one prescribed duration. First select a key with good entanglement fidelity. Then restrict the logical input to a sufficiently large subspace, losing at most one logical qubit. The final worst-case error is at most $`2\sqrt\epsilon`$ when the averaged construction had error $`\epsilon`$. The selected key and subspace may depend on the duration, and no efficient method for finding that subspace is established. This is the separate [expurgation argument](../science/storage_theorem.md#9-deterministic-existence-for-a-prescribed-time).

For distinct positive couplings, an algebraic calculation might initially seem to rule out the mechanism: repeated commutators and Vandermonde inversion recover the individual spin operators, so the associative interaction algebra is the full matrix algebra. Its commutant is scalar, and each fixed finite register eventually depolarizes. The Lie algebra in that argument is a direct sum of local spin algebras, not the full many-body Lie algebra.

The quantitative storage theorem is compatible with those exact algebraic facts. Eventual relaxation at each finite size supplies no size-independent upper bound on the recoverable lifetime. The code exploits increasingly close coefficient groups and final recovery over a specified finite interval. [The symmetry proof](../science/symmetry.md) and [interpretation](../science/interpretation.md) explain that order-of-limits distinction.

## 7. Count the implementation and extend the geometry — M26–M28

Existence of a stabilizer does not provide an efficient way to find or decode it. The repository separates three regimes:

| Guarantee | Endpoint construction established here |
|---|---|
| Fixed rate below one, fixed target error, and a constant times $`n^2`$ storage interval | Polynomial endpoint resources using a fixed Tanner family and an all-size packing argument. |
| Rate approaching one and vanishing error for every $`t_n=o(n^2)`$ | The general outer-code argument is existential. |
| Rate approaching one and vanishing error for $`t_n=o(n^2/\log^3 n)`$ | Polynomial endpoint resources using growing-field CSS Reed–Solomon codes. |

The [resource analysis](../science/resources.md) states the imported coding theorems, length choices, correction thresholds and circuit costs. In the fixed-rate construction, family parameters are constants chosen once for the requested rate and error. In the growing-rate construction, the field size and inner block size grow, so their costs must be included explicitly.

Calibration is also a supplied resource. Certified coefficient errors of order $`1/n`$ suffice to retain the fixed-rate quadratic scaling. Representing that precision takes order $`n\log n`$ classical bits for a bounded list; this is not a bound on the experiments needed to obtain the certificates. Ideal gates, arbitrary endpoint addressing and reliable classical key storage remain assumptions. If encoder and recovery implementations have half-diamond errors $`\delta_E`$ and $`\delta_R`$, channel contraction gives the total budget

```math
\epsilon_{\mathrm{total}}
\le\epsilon_{\mathrm{mem}}+\delta_E+\delta_R.
```

The key register must be included in that composed interface. Polynomial gate counts establish computational scalability in the stated model; they do not establish a fault-tolerant hardware threshold.

The grouping idea also extends to local coupling vectors described by a fixed-dimensional Lipschitz parameter family. With parameter dimension $`r`$, densely occupied cells can have diameter of order $`n^{-1/r}`$ for fixed block parameters. A vector singlet-variance identity then gives an achievable scale $`n^{2/r}`$, and an existential rate-one result for $`t_n=o(n^{2/r})`$. The [geometry proof](../science/coupling_geometry.md) retains a fixed number of Hermitian common fields and no Hamiltonian. It uses the spectral variance argument; the scalar same-axis commutation identity is not assumed for nonparallel local vectors. The exponent is an achievability result for the supplied parameterization, not a claim of intrinsic or optimal dimension.

## 8. What carries the result, and where it stops — M29–M30

The shared-field assumption is consequential. Add independent isotropic depolarization at a fixed rate $`\eta>0`$ on every spin. That channel commutes with the product rotations generated by the common fields. At time $`(\log3)/\eta`$, its one-spin factors are entanglement breaking, hence their tensor product is entanglement breaking. No endpoint recovery can restore quantum entanglement with an inaccessible reference after that loss. An independent classical key does not change the conclusion. The [explicit calculation](../science/examples.md#7-a-fixed-independent-depolarization-rate-stops-the-divergence) states the normalization and factorization.

An entanglement-breaking single-spin marginal under common-field noise alone is a different statement: its global correlated channel may still retain encoded quantum information. The memory guarantee concerns that whole channel and its final recovery.

The contribution therefore rests on a specific chain. A bounded supplied coefficient list provides many close groups. Singlet encoding suppresses each group's common component. The Hermitian generator turns the inherited singlet variance into a finite-time fidelity estimate. Exact marginal closure preserves that estimate inside the correlated register. Keyed Pauli twirling and an outer error-set guarantee convert it into reference-uniform storage at an extensive rate.

Singlet/noiseless codes, concatenation with quantum error correction, the singlet covariance and the coding families are established ingredients. The [related-work account](../references/related_work.md) identifies them and the combined arbitrary-profile storage guarantee. The [verification suite](../verification/README.md) checks finite matrix identities, block dynamics and exhaustive Pauli recovery cases. Those calculations support the derivation and its constants; they do not prove an optimal lifetime or replace the all-size proof. Optimal storage bounds, efficient deterministic expurgation, experimentally acquired calibration and noisy endpoint implementation remain separate questions.

---

[Learning entrypoint](README.md) · [Thirty-milestone map](milestones.md) · [Anchor bridge](anchor_bridge.md) · [Exact theorem](../science/storage_theorem.md) · [Repository entrypoint](../README.md)
