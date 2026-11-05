# Related work and attribution

This comparison concerns the stated noise model and the precise storage interface. The physical register experiences two Hermitian collective generators with one known bounded scalar coupling list, encoding and recovery occur only at the endpoints, and the final error is measured in half diamond distance. Reliable classical records are permitted; a protected quantum bypass is not supplied.

The result combines inherited approximate-decoherence-free-subspace and coding tools with coefficient-space grouping. Its derived statements are the universal fixed-rate quadratic achievable interval, the rate-one existence limit for every $`t_n=o(n^2)`$, and the explicitly accounted endpoint constructions in [resources](../science/resources.md). These are achievability statements. The project does not establish an optimal lifetime.

## 1. Closest DFS and concatenation comparisons

### Lidar, Bacon, and Whaley: DFS–QECC concatenation

**Reference:** [*Concatenating Decoherence Free Subspaces with Quantum Error Correcting Codes*](https://arxiv.org/pdf/quant-ph/9809081), Physical Review Letters **82**, 4556–4559 (1999), arXiv:quant-ph/9809081v2. The relevant parts are the error-correction-on-a-DFS discussion, Eq. (8), and the final perturbative error analysis.

This work constructs DFS inner blocks with an outer quantum error-correcting code and handles leakage. Its example combines four-qubit DFS blocks with the five-qubit code, protecting collective decoherence perturbed by independent decoherence. The concatenation principle and quadratic sensitivity to a symmetry-breaking perturbation are inherited here. The cited construction does not state an arbitrary-coupling-list, asymptotically full-rate storage theorem with an interval approaching quadratic order in register size. The present final-code reduction also allows the residual Pauli errors to remain correlated by a shared field.

### Hwang, Lee, Ahn, and Hwang: imperfect collective pairs

**Reference:** [*Efficient Schemes for Reducing Imperfect Collective Decoherences*](https://arxiv.org/pdf/quant-ph/0008050), Physical Review A **62**, 062305 (2000), arXiv:quant-ph/0008050v4. The relevant model is Eq. (0.6); the procedure following Eq. (0.7) uses repeated measurements.

The paper uses approximately collective pairs, quantum Zeno suppression of leakage, and outer phase-error correction or detection. It is an explicit precedent for protecting imperfectly matched couplings by combining passive and active tools. Its scheme includes interventions during storage and distinct pair baths. It does not give the present endpoint-only, high-rate bound for a common pair of noncommuting fields.

### Kattemölle and van Wezel: dynamical fidelity susceptibility

**Reference:** [*Dynamical fidelity susceptibility of decoherence-free subspaces*](https://arxiv.org/pdf/1809.01261), Physical Review A **99**, 062340 (2019), arXiv:1809.01261v3; Sections II–IV and Lindbladian Appendix B.

This paper establishes generic first-order stability of dynamical fidelity and quantifies the quadratic susceptibility, including its dependence on register size. First-order cancellation alone is therefore not a contribution of this project. The estimate used here is a finite-time bound for a specified, extensive encoded space. A final Pauli-channel reduction then converts marginal entanglement infidelities into a worst-case, reference-uniform memory guarantee. The cited susceptibility result does not itself provide that code or its joint rate/size/time law.

## 2. General Markovian storage and group-transferred channels

### Singh and Datta: peripheral-space storage

**Reference:** [*Information storage and transmission under Markovian noise*](https://arxiv.org/html/2504.10436v2), arXiv:2504.10436v2, Theorem 3.1; published in PRX Quantum **7**, 020312 (2026).

The theorem bounds one-shot storage for powers of a finite-dimensional channel using its peripheral matrix blocks. If their dimensions are $`d_k`$, it gives

```math
Q_\epsilon(\Psi^t)\ge\log_2\max_k d_k,
```

and, once $`\epsilon+\delta_t\lt 1`$,

```math
Q_\epsilon(\Psi^t)
\le\log_2\max_kd_k+
\log_2\frac1{1-\epsilon-\delta_t},
\qquad
\delta_t=\|\Psi^t-\Psi_\infty^t\|_\diamond.
```

For the distinct positive couplings considered here, the stationary algebra is scalar, so its peripheral-space achievable lower bound is zero. Its eventual converse remains relevant at fixed register size. Obtaining a uniform size-dependent time from it requires control of the channel-dependent convergence parameters. The cited theorem does not supply the present extensive lower bound before mixing.

### Bardet and collaborators: transference and capacity bounds

**Reference:** [*Group transference techniques for the estimation of the decoherence times and capacities of quantum Markov semigroups*](https://arxiv.org/pdf/1904.11043), IEEE Transactions on Information Theory **67**(5), 2878–2909 (2021), arXiv:1904.11043v2; collective-decoherence examples and Theorems V.2 and V.9.

The paper transfers classical compact-group mixing estimates to quantum decoherence and capacity estimates. Its achievable bounds use the fixed algebra; its finite-time upper bounds depend on mixing or logarithmic-Sobolev constants. Its worked collective-spin examples use equal-weight representations. The weighted two-generator model here fits a group-transferred description on $`SU(2)^n`$, but this observation does not provide its size-dependent geometric constants or an extensive achievable code. The common stochastic-unitary viewpoint and general fixed-algebra framework are inherited background.

## 3. Comparison with Quantum Spectral Memory

The comparison uses the repository snapshot at commit [`ee5dc0e5529c7775bfaeabb2a5e744c51eb9431d`](https://github.com/GoGoKo699/Quantum-Spectral-Memory/tree/ee5dc0e5529c7775bfaeabb2a5e744c51eb9431d), inspected on 2026-11-05. In particular, the [operational model](https://github.com/GoGoKo699/Quantum-Spectral-Memory/blob/ee5dc0e5529c7775bfaeabb2a5e744c51eb9431d/science/model.md), [spectral-law Theorem 1](https://github.com/GoGoKo699/Quantum-Spectral-Memory/blob/ee5dc0e5529c7775bfaeabb2a5e744c51eb9431d/science/spectral_law.md), and [finite-precision encoder](https://github.com/GoGoKo699/Quantum-Spectral-Memory/blob/ee5dc0e5529c7775bfaeabb2a5e744c51eb9431d/science/encoder.md) were compared.

| Aspect | Quantum Spectral Memory at the pinned commit | Present model |
|---|---|---|
| Generator | One known Hermitian operator | Two noncommuting weighted spin sums |
| Structure used | Gaussian Schur channel in one eigenbasis | Nearby coupling groups and spin-zero sectors |
| Main bound | Matching spectral-occupancy storage bounds at fixed error | Achievable rate and lifetime bounds |
| Constructive ingredient | Calibrated spectral-band compiler | Singlet inner maps and endpoint outer correction |
| Boundary interface | Arbitrary encoders, recoveries, and classical records | The same type of interface, with the Pauli key charged explicitly |

The earlier theorem states that the optimal stored log dimension agrees, up to an error-dependent constant, with the logarithm of the maximum number of eigenvalues inside a width-$`t^{-1/2}`$ interval. Its single-generator Schur-channel argument does not apply directly to the two noncommuting operators here. Conversely, this project does not inherit that theorem's matching converse or its constant-qubit optimality guarantee.

## 4. Coding and circuit ingredients used directly

The outer codes and their decoding algorithms are existing constructions:

- Leverrier–Zémor, [*Quantum Tanner codes*](https://arxiv.org/html/2202.13641v3), Theorems 17–18, supplies the high fixed rates and local-code existence.
- Leverrier–Zémor, [*Decoding quantum Tanner codes*](https://arxiv.org/html/2208.05537v3), Theorem 6 and Theorem 13, supplies product-expanding local codes and the adversarial-error decoder used here.
- Dinur et al., [arXiv:2111.04808v2](https://arxiv.org/pdf/2111.04808), Section 6.2 and Claim 6.7, supplies the explicit group family behind the Tanner lengths. The greedy all-size packing and its error accounting are proved in the resource account.
- Grassl–Geiselmann–Beth, [*Quantum Reed–Solomon Codes*](https://arxiv.org/pdf/quant-ph/9910059), provides the finite-field quantum-code and circuit framework. The resource account states and derives the particular nested evaluation-code parameters it uses.
- Gottesman, [*Stabilizer Codes and Quantum Error Correction*](https://arxiv.org/html/quant-ph/9705052v1), Sections 4.1–4.3 and Eq. (4.26), supplies standard-form encoding and its quadratic gate bound.
- Barenco et al., [*Elementary gates for quantum computation*](https://arxiv.org/abs/quant-ph/9503016), and Dawson–Nielsen, [*The Solovay–Kitaev algorithm*](https://arxiv.org/html/quant-ph/0505030v2), supply finite-unitary decomposition and compilation to a fixed universal gate set.

These ingredients are attributed independently of the storage theorem. The explicit resources distinguish a fixed-rate polynomial Tanner construction from the separate growing-rate Reed–Solomon construction. Neither the existence of a good code nor an efficient inner encoder alone establishes an efficient full memory protocol.

## 5. Related sensing and the single-spin diagnostic

Urizar-Lanz et al., [*Macroscopic singlet states for gradient magnetometry*](https://www.gtoth.eu/Publications/PRA13_singlet.pdf), Physical Review A **88**, 013626 (2013), Eqs. (10), (16)–(18), identifies the normalized full-singlet projector and its one- and two-spin marginals. These imply the scalar and vector second-moment identities used here; those identities are inherited. The paper studies gradient sensing. This project uses the moments in a finite-time Markovian survival bound, then combines coefficient-space grouping and correlated-error recovery to derive its memory guarantees. The $`n^{2/r}`$ geometry corollary makes no separate priority claim for singlet moments or geometric packing.

Hamann–Sekatski–Dür, [*Approximate decoherence free subspaces for distributed sensing*](https://arxiv.org/html/2106.13828v1), Quantum Science and Technology **7**, 025003 (2022), uses known spatial dependence to design exact and approximate protected sensing subspaces. Its main scalar-field setting and two-dimensional sensing encoding motivate quantitative control of coupling mismatch. The task is sensing rather than extensive unknown-state storage under the two noncommuting fields used here.

Ruskai, [*Qubit Entanglement Breaking Channels*](https://arxiv.org/html/quant-ph/0302032v3), Reviews in Mathematical Physics **15**, 643–662 (2003), **Theorem 4**, states that a unital qubit channel with canonical Bloch multipliers $`\lambda_j`$ is entanglement breaking exactly when $`\sum_j|\lambda_j|\le1`$. Applying it to the isolated-spin multipliers

```math
(e^{-2g^2t},e^{-4g^2t},e^{-2g^2t})
```

gives the threshold $`t=\ln(1+\sqrt2)/(2g^2)`$ used in [the interpretation](../science/interpretation.md). This is a local diagnostic. The many-spin common-field channel is not the tensor product of its one-spin marginals, so the local threshold is not a converse for collective storage.

## 6. Scope of the comparison

The combination of singlet encoding, approximate DFS protection, Pauli randomization, and outer correction has established antecedents. The statements developed here concern how a supplied bounded coefficient list can be organized into a reference-uniform memory protocol, with its size dependence, retained key, finite precision, and endpoint costs stated together.

The comparisons above identify what the inspected primary results do and do not state. They do not constitute an exhaustive priority claim. No hardware threshold, robustness to a fixed independent-noise floor, or optimal-time converse follows from the present achievability proof.

[Bibliography](references.bib) · [Storage theorem](../science/storage_theorem.md) · [Resources](../science/resources.md)
