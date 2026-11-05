# From Nielsen–Chuang to the storage theorem

An unknown quantum state can carry information in its correlations with another system. A useful memory must preserve those correlations as well as the state of the register itself. Nielsen–Chuang supplies the language of composite systems, noisy channels and quantum error correction. The bridge developed here connects that language to a specific question: how can a register retain an extensive quantum payload for a growing interval when distinct couplings remove its exact noiseless symmetry?

## 1. The selected educational anchor

**Michael A. Nielsen and Isaac L. Chuang, _Quantum Computation and Quantum Information_, 10th Anniversary Edition, Cambridge University Press.** The edition is identified as 2010 in the publisher's front matter; the hardback ISBN is **9781107002173** and the book DOI is [10.1017/CBO9780511976667](https://doi.org/10.1017/CBO9780511976667).

The [official front matter and detailed contents](https://assets.cambridge.org/97811070/02173/frontmatter/9781107002173_frontmatter.pdf) give the section and printed-page pointers below. The current PDF identifies itself as version 16, July 2025. The [publisher's catalog](https://www.cambridge.org/highereducation/books/quantum-computation-and-quantum-information/01E10196D0A682A6AEFFEA52D53BE9AE/contents/729A1063B8E18926B2B83C43A9D3F892) separately dates the hardback to 31 January 2011.

| Foundation | Anchor sections and printed pages | Use in this project |
|---|---|---|
| Composite states, marginal states and purification | §§2.2.8, 2.4.3, 2.5; pp. 93, 105, 109 | Define the physical register, inaccessible reference and partial trace in the [operational model](../science/model.md). |
| Environment and operator-sum descriptions of channels | §§8.2.2–8.2.4; pp. 357, 360, 366 | Describe encoding, noise, recovery and the trace-preserving leakage decoder. |
| Continuous-time noise | §8.4.1; p. 386 | Interpret the specified generator and its semigroup in [model §1](../science/model.md#1-register-coefficients-and-time-convention). |
| State distances, fidelity and channel preservation | §§9.2.1–9.2.3, 9.3; pp. 403, 409, 415, 416 | Separate the block fidelity estimate from the complete memory error in [theorem §§3–6](../science/storage_theorem.md#3-exact-local-diamond-norm-estimate). |
| Error sets and recovery | §§10.3–10.3.3; pp. 435, 438, 441, 444 | Connect arbitrary Pauli-error correction with the correlated distribution in [theorem §§6–7](../science/storage_theorem.md#6-global-pauli-twirling-and-correlated-error-correction). |
| CSS and stabilizer constructions | §§10.4.2, 10.5; pp. 450, 453 | Identify the outer-code framework; the actual code families and bounds are in [resources](../science/resources.md). |
| Encoding and recovery circuits | §10.5.8; p. 472 | Relate algebraic encoders to the counted endpoint operations in [resources §§4–5](../science/resources.md#4-endpoint-circuit-and-classical-computation-accounting). |

The verification scope is the publisher's edition information and detailed table of contents, rather than a full-text audit of the chapter proofs. The specialized singlet/noiseless-subsystem construction and diamond-norm argument are supplied in the project pages; the verified contents do not establish their treatment in the book. Definitions below state this repository's conventions explicitly.

The primary research attribution remains in [related work](../references/related_work.md), the [bibliography](../references/references.bib), and the scientific proofs. A derivation supplied here may use an established ingredient; its presence in this bridge does not make that ingredient a new result.

## 2. Notation and convention translation

The anchor's channel and coding concepts enter this project through the following concrete objects.

| Concept | Project notation and convention |
|---|---|
| Physical carrier | $`n`$ noisy qubits. Unused spins still count in the rate denominator $`k/n`$. |
| Inner and outer encodings | $`K`$ inner blocks, each containing $`m`$ physical spins and $`k_m`$ inner logical qubits. The outer code acts on $`M=Kk_m`$ qubits and carries $`k`$ final logical qubits. |
| Operator-sum description | Write a generic channel as $`\mathcal N(X)=\sum_a K_aXK_a^\dagger`$, with $`\sum_aK_a^\dagger K_a=I`$. The symbol $`E_b`$ is reserved for an inner encoding isometry, not a generic error operator. |
| Spin normalization | $`X_j,Y_j,Z_j`$ have eigenvalues $`\pm1`$. The block sum $`J_{\alpha,b}=\sum_{j\in b}\sigma_{\alpha,j}`$ is twice the conventional angular-momentum component. Both annihilate a singlet. |
| Continuous-time channel | $`\Phi_{n,t}=e^{t\mathcal L_n}`$, with Hermitian jumps and no extra Hamiltonian. The positive rates $`\gamma_x,\gamma_z`$ are fixed as $`n`$ grows; $`\Gamma=\gamma_x+\gamma_z`$. |
| Error weight | The main outer code corrects up to $`h`$ nonidentity **single-qubit** Pauli factors among its $`M`$ inputs. A bad inner block can contribute as many as $`k_m`$ such factors. |
| Randomization | A key $`\kappa`$ selects boundary Pauli conjugations and uses $`2M`$ reliable classical bits. The guarantee is for the resulting averaged channel, with a worst case over logical inputs and references. |

The Pauli normalization fixes the time units. With

```math
\begin{gathered}
A_x=\sum_jg_jX_j,\qquad A_z=\sum_jg_jZ_j,\qquad 1\le g_j\le2,\\
\mathcal D[A](X)=AXA-\frac12\{A^2,X\},
\qquad
\mathcal L_n=\gamma_x\mathcal D[A_x]+\gamma_z\mathcal D[A_z].
\end{gathered}
```

replacing every Pauli by a spin operator one half as large divides its dissipator by four. A change of spin convention therefore requires a corresponding change of rates. No division of the collective jumps by $`n`$ or $`\sqrt n`$ is part of the model.

### Fidelity and complete-channel error

For a decoded block channel $`\mathcal N_b`$ on $`d=2^{k_m}`$ dimensions, let $`\omega_d`$ be the normalized maximally entangled state of the logical block and a reference. This project uses the **overlap convention**

```math
F_{e,b}
=\mathrm{Tr}\!\left[
\omega_d(\mathcal N_b\otimes\mathrm{id})(\omega_d)
\right],
\qquad p_b=1-F_{e,b}.
```

If fidelity is instead written in root form,
$`F_{\mathrm{root}}(\rho,\sigma)=\|\sqrt{\rho}\sqrt{\sigma}\|_1`$,
its square is the overlap when one argument is pure. Thus the root fidelity of this Bell-state comparison is $`\sqrt{F_{e,b}}`$. The exponential bound in the proof controls $`1-F_{e,b}`$.

The final criterion has a different quantifier. For the recovered logical channel $`\mathcal M_{n,t}`$,

```math
\begin{aligned}
\epsilon_{\mathrm{mem}}
&=\frac12\|\mathcal M_{n,t}-\mathrm{id}_{2^k}\|_\diamond\\
&=\sup_{\rho_{LR}}
\frac12\left\|
(\mathcal M_{n,t}\otimes\mathrm{id}_R)(\rho_{LR})
-\rho_{LR}
\right\|_1 .
\end{aligned}
```

Here $`L`$ is the $`k`$-qubit logical input, and a reference $`R`$ of dimension $`2^k`$ suffices. The trace norm is the sum of singular values. This definition asks for preservation of every input and its entanglement with an inaccessible reference. A high Bell-state fidelity by itself is not identified with this worst-case channel guarantee. The recovery argument below supplies the connection used by the theorem.

## 3. Additional steps supplied by the project

### Closely matched couplings supply an approximate singlet code

The textbook channel framework specifies how a given noisy process acts. The next step is to exploit the supplied coefficient list. Choose even $`m\ge4`$ and $`C>1`$ with $`n\ge2Cm`$; the parameter $`C`$ controls the discarded fraction. Binning $`[1,2]`$ into $`B=\lfloor n/(Cm)\rfloor`$ cells loses at most $`B(m-1)\le n/C`$ spins when forming complete blocks. Every list therefore provides an extensive set of narrow-coupling blocks.

Within each block, the equal-coupling part of both collective fields annihilates the total-spin-zero sector. Its dimension is

```math
D_m=\frac{1}{m/2+1}\binom m{m/2},
\qquad
k_m=\lfloor\log_2D_m\rfloor,
\qquad
\rho_m=\frac{D_m}{2^{k_m}}\lt 2.
```

The factor $`\rho_m`$ accounts for selecting a qubit-sized logical space within that sector. The cancellation and dimension count are established singlet facts, derived and attributed in [theorem §2](../science/storage_theorem.md#2-binning-and-the-singlet-code). The additional grouping argument makes them useful for every supplied bounded coefficient list.

### A singlet variance gives a finite-time fidelity bound

A perturbative loss rate at time zero does not alone establish a long storage interval. [Theorem §4](../science/storage_theorem.md#4-sharper-marginal-entanglement-infidelity-bound) uses the Hermitian-jump generator's self-adjointness and negativity in Hilbert–Schmidt inner product. The encoded Bell-state survival is a positive mixture of decaying exponentials. Jensen's inequality then turns its initial mean loss rate into a bound valid for every time:

```math
p_b\le1-e^{-\mu_bt}\le\mu_bt,
\qquad
\mu_b=\Gamma\rho_m\frac{m}{m-1}
\sum_{j\in b}(g_j-\bar g_b)^2.
```

Here $`\bar g_b`$ is the mean coupling within block $`b`$. Permutation invariance of the full singlet projector supplies the variance identity. Positivity supplies the comparison with the selected logical subspace, including the factor $`\rho_m`$. The decoder maps leakage to a fixed state, so it remains a channel on every possible output. The separate restricted-generator estimate in [theorem §3](../science/storage_theorem.md#3-exact-local-diamond-norm-estimate) is a local diamond-norm statement; its role and bound are different.

### Exact marginals retain the common-field correlations

Partial trace does more here than define a reduced state. For each Hermitian one-body collective jump, the double-commutator form of the dissipator gives the intertwining identity

```math
\mathrm{Tr}_{T}\circ\Phi_{n,t}
=\Phi_{S,t}\circ\mathrm{Tr}_{T},
\qquad T=S^{\mathrm c}.
```

Consequently, the isolated-block calculation gives the exact marginal channel even for inputs entangled across blocks. The full channel still has correlated errors. [Theorem §5](../science/storage_theorem.md#5-exact-non-signalling-and-unused-spins) proves the identity and justifies discarding unused spins. The independent-error model discussed in anchor §10.3.2 is an additional assumption that this storage proof does not make.

### Error correction converts a marginal probability into a reference-uniform guarantee

Pauli twirling at the endpoints removes cross terms in the Kraus expansion and produces a joint Pauli distribution. It preserves the block entanglement fidelities, so $`p_b`$ becomes exactly the marginal probability of a nonidentity Pauli on block $`b`$. No factorization of that distribution is required.

For a joint Pauli error $`Q`$, an outer code correcting all weights up to $`h`$ gives

```math
\mathbb E[\mathrm{wt}(Q)]
\le k_m\sum_b p_b,
\qquad
\Pr(\mathrm{wt}(Q)>h)
\le\frac{k_m}{h+1}\sum_b p_b.
```

Every error in the complementary event is corrected for every logical input, including its reference. The recovered channel is a convex mixture of the identity and a failure-branch channel. Its half-diamond error is therefore at most that failure probability. This is the decisive link from the block fidelity to the memory theorem. [Theorem §§6–7](../science/storage_theorem.md#6-global-pauli-twirling-and-correlated-error-correction) provide the twirl, weight accounting and finite stabilizer existence proof.

### Exact finite-size symmetry and growing storage time answer different questions

For distinct positive coefficients, repeated commutators and a Vandermonde inversion recover all individual Pauli operators. Their products span the full associative interaction algebra. [The symmetry proof](../science/symmetry.md) consequently gives a scalar commutant and eventual depolarization at each fixed $`n`$. It does not give a mixing rate uniform in $`n`$. The storage theorem instead controls a finite interval while the register size grows. This additional algebraic argument explains why its approximate codes are compatible with the absence of an exact noiseless subsystem.

## 4. Where the bridge reaches the theorem

At fixed block size, discard parameter and outer correctable fraction, bin width is $`O(1/n)`$. The variance bound is then $`O(t/n^2)`$, and outer recovery tolerates a fraction of errors. [Theorem §8](../science/storage_theorem.md#8-explicit-asymptotic-consequences) makes the constants and roundings explicit: every fixed rate $`0\lt R\lt 1`$ and fixed target error admit a sufficiently small constant times $`n^2`$ storage interval. A separate parameter sequence gives rate approaching one and error approaching zero for every $`t_n=o(n^2)`$. These are achievable guarantees.

The existence argument does not by itself supply an efficient decoder. [Resources](../science/resources.md) supplies polynomial endpoint constructions at fixed rate using an existing Tanner family, and a separate growing-rate Reed–Solomon construction for $`t_n=o(n^2/\log^3 n)`$. It also counts calibration precision, classical key storage, circuit synthesis and additive boundary errors. Those claims use explicit research-level coding ingredients; they are not consequences inferred solely from the textbook circuit section.

The interval begins after encoding and ends before recovery. Supplied calibration, ideal storage-model dynamics and reliable classical records are part of its interface. Implementing noisy endpoints, adding a fixed independent local-noise floor, or proving an optimal lifetime requires the distinctions stated in [the model](../science/model.md) and [interpretation](../science/interpretation.md).

[Learning overview](README.md) · [Milestone map](milestones.md) · [Continuous tutorial](tutorial.md)

[Scientific overview](../science/README.md) · [Exact storage theorem](../science/storage_theorem.md) · [Attribution](../references/related_work.md) · [Repository entrypoint](../README.md)
