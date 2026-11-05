# Noise model and operational task

The task is to preserve an unknown quantum state in a noisy register while leaving that register untouched during storage. The encoder and the final recovery may act jointly on many spins. The theorem concerns the amount of quantum information recovered at the endpoint, including its entanglement with an inaccessible reference.

The central distinction is between exact symmetry at a fixed register size and reliable storage as that size grows. For distinct couplings, the interaction algebra in this model has no nontrivial noiseless subsystem. Nevertheless, [the storage theorem](storage_theorem.md) constructs codes with a diverging storage interval and an extensive number of logical qubits. The interval proved there is achievable; its optimality is not established.

## 1. Register, coefficients, and time convention

There are $`n`$ physical qubits with Hilbert space

```math
\mathcal H_n=(\mathbb C^2)^{\otimes n}.
```

The real coefficients $`g_1,\ldots,g_n`$ are known and satisfy

```math
1\le g_j\le 2.
```

No distribution, ordering, minimum spacing, or approximate equality between the coefficients is assumed. They may repeat. The code is allowed to depend on their supplied values. A particularly transparent admissible instance is the deterministic profile $`g_j=1+j/n`$.

Let $`X_j,Y_j,Z_j`$ denote Pauli matrices on spin $`j`$, with identity on every other spin. We use Pauli matrices with eigenvalues $`\pm1`$, rather than spin operators with eigenvalues $`\pm1/2`$. Define

```math
A_x=\sum_{j=1}^n g_jX_j,\qquad
A_z=\sum_{j=1}^n g_jZ_j.
```

The register evolves under the time-homogeneous Markov semigroup

```math
\Phi_{n,t}=e^{t\mathcal L_n},\qquad
\mathcal L_n
=\gamma_x\mathcal D[A_x]+\gamma_z\mathcal D[A_z],
\qquad
\mathcal D[A](\rho)
=A\rho A-\frac12\{A^2,\rho\}.
```

Throughout, $`\gamma_x,\gamma_z>0`$ are fixed constants, independent of $`n`$. Write $`\Gamma=\gamma_x+\gamma_z`$. There is no additional system Hamiltonian in the main theorem. In particular, the collective operators are not divided by $`n`$ or $`\sqrt n`$, and the noise strengths do not decrease as the register grows.

The interval $`[1,2]`$ fixes the units and keeps the single-spin noise strength away from zero. The storage proof also applies to a supplied list in any fixed interval $`[a,b]`$: each squared block-width bound gains a factor $`(b-a)^2`$. That extension keeps both the interval and the rates fixed as $`n`$ grows. Statements about the absence of exact symmetry additionally require nonzero coefficients with distinct absolute values.

## 2. What the common-field assumption means

The two jumps are Hermitian sums of one-spin terms. Equivalently, the register is driven by two common classical white-noise fields. Let $`W_x,W_z`$ be independent standard Brownian motions. For a coefficient $`g`$, define the one-spin stochastic unitary by the Itô equation

```math
dU_g(t)
=-ig\sum_{\alpha\in\{x,z\}}\sqrt{\gamma_\alpha}\,
       \sigma_\alpha U_g(t)\,dW_\alpha(t)
  -\frac12g^2\Gamma U_g(t)\,dt,
\qquad U_g(0)=I.
```

The same two paths drive every spin. Conditional on those paths, the register unitary is

```math
U_{\boldsymbol g}(t)=\bigotimes_{j=1}^n U_{g_j}(t).
```

Itô's product rule gives

```math
\Phi_{n,t}(\rho)
=\mathbb E\!\left[
U_{\boldsymbol g}(t)\rho U_{\boldsymbol g}(t)^\dagger
\right].
```

The cross terms in that product rule produce the collective dissipators above. The local unitary factors are therefore strongly correlated random variables. Replacing this model by independent noise on the spins, or by independent noise on the eventual coding blocks, would change the channel.

This representation explains the physical origin of the correlations. The proof in [storage_theorem.md](storage_theorem.md) instead uses an exact partial-trace identity for the generator, so it does not need to assume a particular measurement or access to the Brownian paths.

## 3. Permitted operations and the error criterion

An encoder takes $`k`$ logical qubits into the register. A recovery maps the register back to those $`k`$ qubits after time $`t`$. All quantum ancillas used for encoding or recovery are endpoint resources. During the open storage interval there are no controls, measurements, resets, replenished ancillas, or retained quantum systems carrying part of the input.

The constructive proof uses classical randomization. A uniformly random Pauli key $`\kappa`$ is chosen independently of the input and the noise. The encoder and recovery know that key. The protocol keeps $`2M\le2n`$ classical bits, where $`M`$ is the number of inner logical qubits. The key carries no quantum payload. Reliability of this classical record is an assumption, separate from reliability of the noisy spin register.

For key-dependent encoder $`\mathcal E_\kappa`$ and recovery $`\mathcal R_\kappa`$, the implemented logical channel is

```math
\mathcal M_{n,t}
=\mathbb E_\kappa\!
\left[\mathcal R_\kappa\circ\Phi_{n,t}\circ\mathcal E_\kappa\right].
```

Its error is

```math
\epsilon_{\mathrm{mem}}(n,t)
=\frac12\left\|\mathcal M_{n,t}-\operatorname{id}_{2^k}
\right\|_\diamond.
```

Thus the guarantee is worst case over the logical input and every entangled reference, and averaged over the protocol's classical coins. It is not a guarantee for every individual key. The key is independent of the input; the channel does not adapt adversarially to that key.

The proof also gives a deterministic existence result for each prescribed storage time. It fixes one key and restricts the logical space, losing at most one logical qubit and replacing error $`\epsilon`$ by at most $`2\sqrt\epsilon`$. Finding the required subspace efficiently is not proved. The deterministic result and its time dependence are stated separately in [Section 9 of the theorem](storage_theorem.md#9-deterministic-existence-for-a-prescribed-time).

Some physical spins are left unused when forming blocks. They remain included in the denominator of the storage rate $`k/n`$. They can be initialized in any fixed state and discarded at the output. An exact non-signalling identity shows that their presence cannot alter the channel on the retained spins.

## 4. Consequence of the theorem

For every fixed target rate $`R<1`$ and error $`0<\epsilon<1`$, the theorem supplies constants $`c_{R,\epsilon}>0`$ and $`n_0`$ such that every supplied coefficient list in $`[1,2]^n`$, with $`n\ge n_0`$, admits storage of at least $`Rn`$ logical qubits with

```math
\epsilon_{\mathrm{mem}}(n,t)\le\epsilon
\qquad\text{for every}\qquad
0\le t\le c_{R,\epsilon}n^2.
```

The randomized encoder and recovery in this statement are fixed across that entire interval. In addition, for every sequence $`t_n=o(n^2)`$, there are codes whose rate tends to one and whose error tends to zero. The Gilbert–Varshamov construction in the main proof is an existence argument for the outer code and decoder; a computational implementation claim requires the separate outer-code analysis.

The comparison with an isolated spin uses the same rates and coefficients. Its three Bloch components evolve as

```math
(r_x,r_y,r_z)\longmapsto
\left(
e^{-2\gamma_z g^2t}r_x,\,
e^{-2\Gamma g^2t}r_y,\,
e^{-2\gamma_x g^2t}r_z
\right).
```

Since $`g\in[1,2]`$ and both rates are fixed, every component decays on a time scale bounded independently of $`n`$. The growing encoded storage interval comes from information stored across spins with closely matched couplings, followed by final error correction.

For distinct positive coefficients, [symmetry.md](symmetry.md) proves that the generated associative interaction algebra is the entire matrix algebra. Its Lie algebra is the direct sum of the local $`\mathfrak{su}(2)`$ algebras; these are different statements. The interaction commutant is scalar and the finite-register semigroup eventually depolarizes. That exact finite-size fact is compatible with a storage interval that grows with size.

## 5. Inherited ingredients and the scope of the claim

Singlet encoding under exactly collective noise is an established noiseless-code construction, going back to [Zanardi and Rasetti, *Noiseless Quantum Codes* (1997)](https://arxiv.org/abs/quant-ph/9705044). Combining a decoherence-free inner code with outer quantum error correction, including recovery from leakage, is also established; see [Lidar, Bacon, and Whaley, *Concatenating Decoherence Free Subspaces with Quantum Error Correcting Codes* (1999)](https://arxiv.org/abs/quant-ph/9809081).

The derived statement here is the uniform size–rate–time guarantee for arbitrary supplied bounded coupling lists under this actual correlated, noncommuting noise model. The proof makes the block mismatch small by grouping close coefficient values, bounds its finite-time channel effect, and converts correlated residual errors into an endpoint coding guarantee.

The theorem assumes ideal endpoint operations and supplied coefficient values. It does not establish a calibration procedure, fault tolerance of those operations, an optimal lifetime, protection against a fixed independent local-noise floor, or storage under an arbitrary quantum bath. Those are separate physical and computational questions.

[Coupling geometry](coupling_geometry.md) extends the storage argument to a fixed number of Hermitian common fields whose local amplitudes and directions form a supplied Lipschitz parameter family. That corollary keeps the same storage interface and no-Hamiltonian assumption; the full-algebra statement above remains specific to the original scalar model.
