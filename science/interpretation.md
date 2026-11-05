# Why a primitive collective channel can retain a large quantum memory

The [storage theorem](storage_theorem.md) concerns a family of increasingly large registers at a specified storage time. It exhibits a separation between the exact algebra of a finite noisy system and the amount of quantum information that can survive before that system mixes. The distinction is operational: the recovered state must preserve every logical input, including entanglement with an inaccessible reference.

## The scale comes from the coupling values

Suppose every physical spin has a coupling in the fixed interval $`[1,2]`$. Adding spins does not weaken the noise seen by an individual spin. It does, however, place more coupling values in the same bounded interval. A partition into sufficiently narrow bins therefore finds many small groups of nearly equally coupled spins, for every coefficient list. There is no distributional assumption on that list.

Within a group, the equal-coupling part of each field is a collective rotation. A singlet sector is fixed by every such rotation, including rotations about noncommuting axes. The residual disturbance depends on the spread of couplings within the group. Its mean-square size, and hence the block's entanglement-infidelity rate, is quadratic in that spread.

At a fixed encoding rate, the block size and tolerated discarded fraction can be held constant. The bin width is then proportional to $`1/n`$, so a block has an error bound proportional to $`t/n^2`$. This is the origin of the quadratic achievable storage scale. It is a consequence of increasingly dense coupling values, not a noise-rate normalization that decreases with $`n`$.

The grouping may connect spins far apart in real space. Coupling-space proximity and geometric proximity are different resources. The theorem permits nonlocal boundary operations and imposes no spatial layout constraint.

## Why a final recovery changes the time scale

Protecting the entire encoded state directly requires the accumulated error over all blocks to remain small. A final quantum error-correcting code instead tolerates errors on a nonzero fraction of its inputs. The latter task uses the single-block disturbance scale without paying an additional factor proportional to the number of blocks.

The common fields correlate the errors. The proof does not replace them by independent noise. Random Pauli conjugations at the boundaries produce a correlated Pauli distribution. A bound on its expected error weight, together with a code that corrects every error below a fixed weight, is enough to bound the probability of failed recovery. Every correctable Pauli is corrected for every logical input, which is why the resulting bound is in half-diamond distance.

This use of singlet sectors and outer quantum correction builds on established decoherence-free-subspace coding. The [related-work account](../references/related_work.md) identifies the inherited construction and the additional arbitrary-profile rate/time statement. No new error-correction threshold or decoder is asserted.

## Exact symmetry and finite-time storage are different statements

For pairwise-distinct positive coefficients, [the commutator calculation](symmetry.md) recovers each single-spin Pauli operator from the weighted collective generators. Their associative operator algebra is consequently the full matrix algebra. Its commutant is scalar, so there is no nontrivial exact noiseless subsystem. The unique stationary state is maximally mixed.

The Lie algebra and associative algebra must be distinguished here. Commutators of one-body operators remain one-body; the dynamical Lie algebra is a direct sum of single-spin $`\mathfrak{su}(2)`$ algebras. Products of those recovered operators generate the full many-qubit associative algebra. The latter fact supplies the fixed-algebra conclusion.

At every fixed $`n`$, sufficiently long storage eventually loses the information. The achievable theorem instead lets the register size grow while choosing a storage time below the established size-dependent scale. No interchange of an infinite-time limit and a large-system limit is used.

For comparison, an isolated spin with coupling $`g`$ and unit noise rates has Bloch multipliers

```math
\left(e^{-2g^2t},\ e^{-4g^2t},\ e^{-2g^2t}\right).
```

The unital qubit channel is entanglement breaking when the sum of these multipliers is at most one. This occurs at

```math
t_{\mathrm{EB}}(g)=\frac{\log(1+\sqrt2)}{2g^2}.
```

Thus each individual carrier loses the ability to preserve entanglement after a size-independent time, while the encoded register has a diverging achievable storage time. The [model](model.md) gives the Bloch multipliers, and the [examples](examples.md) explain the entanglement-breaking criterion and provide finite checks. This comparison uses the same unscaled physical noise rates.

## What the implementation guarantees mean

There are separate statements about existence and boundary complexity:

| Statement | Boundary resources |
|---|---|
| Any fixed rate below one and fixed error at a sufficiently small constant times $`n^2`$ | Polynomial encoding and recovery using a fixed-rate family of existing quantum Tanner codes; constants depend on the selected rate and error. |
| Rate approaching one and vanishing error for every $`t=o(n^2)`$ | Information-theoretic construction; an arbitrary distance-code decoder need not be efficient. |
| A growing-rate explicit construction | A quantum Reed–Solomon construction and its precise logarithmic time loss are given in [resources](resources.md). |

The direct randomized implementation retains $`2M`$ reliable classical bits for $`M`$ inner logical qubits. The key is independent of the unknown quantum input and carries no quantum payload. The error guarantee is for the complete decoded channel averaged over that key. It is not a worst-case assertion for every key value. Deterministic expurgation removes the retained key for an existence theorem at each prescribed storage time, with at most one logical qubit lost; an efficient construction of that expurgated subspace is not established.

Calibration is supplied through estimates and certified error bounds. Describing a coupling to order $`1/n`$ accuracy uses logarithmically many classical bits at fixed range. That statement does not determine the number of experiments, preparation time, or physical reference stability needed to obtain the certificate.

The interval starts after encoding and ends before recovery. These operations may use temporary quantum workspace, initialization and measurements; the only quantum carrier across the interval is the noisy physical register. A polynomial circuit bound does not show that an implementation can finish under continuing noise, meet a fault-tolerance threshold, or outperform a particular device. The composable boundary-error budget in [resources](resources.md) states the additional implementation accuracy required.

## The independent-noise boundary

The collective correlations are a physical assumption. In particular, adding a fixed rate of independent isotropic depolarization rules out a diverging storage time in this model. Local isotropic depolarization commutes with every product-unitary realization of the collective channel. Once each local depolarizing channel is entanglement breaking, its tensor product is entanglement breaking on the entire register, and subsequent collective evolution and recovery cannot restore entanglement with an inaccessible reference.

This obstruction also allows arbitrary retained classical records: each conditional encoded branch becomes separable from the reference, and summing the classical branches preserves separability. It is therefore not an artifact of the particular singlet construction. The [examples and boundary calculation](examples.md) state the normalization and derive the quantitative limit.

## Established scale and open optimality

The result is an achievable storage law. It does not prove that $`n^2`$ is the longest possible scale for every bounded distinct coefficient list. Some lists have exact degeneracies, unusually small spacings, or larger protected approximate sectors. A converse would need to account for those features and for arbitrary encoders and recoveries.

The uniform statement deliberately avoids such spectral promises: every bounded list admits the specified code. The explicit equally spaced profile demonstrates the construction under a transparent calibration convention. Neither that example nor a small-system numerical spectrum establishes an optimal lifetime.

[Scientific overview](README.md) · [Model](model.md) · [Storage proof](storage_theorem.md) · [Resources](resources.md)
