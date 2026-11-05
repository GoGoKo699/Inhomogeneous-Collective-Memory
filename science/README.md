# Scientific overview

The question is how much unknown quantum information can survive common noise whose coupling to each spin is different. Exact noiseless-subsystem theory gives a discouraging answer for generic distinct couplings: the interaction algebra is full. The finite-time answer is different. A large supplied coefficient list necessarily admits many small groups of closely matched spins, and these groups support approximate singlet memories with final outer correction.

The main result is uniform over every bounded coefficient list in the stated model. At any fixed rate below one, the achieved storage interval is proportional to the square of register size. A separate limiting construction makes the rate approach one and the error vanish at every subquadratic time. These are lower bounds on what can be stored; the optimal lifetime is not determined.

## Read the connected account

| Scientific question | Authoritative page |
|---|---|
| What channel, resources, and error criterion are being studied? | [Noise model and operational task](model.md) |
| How can an extensive state survive for a quadratic interval? | [Finite-size storage theorem and complete proof](storage_theorem.md) |
| Why is there no exact noiseless subsystem for distinct couplings? | [Interaction algebra and finite-size mixing](symmetry.md) |
| What does a practical endpoint claim need to count? | [Calibration, code construction, and endpoint resources](resources.md) |
| What changes when field amplitudes or directions have several parameters? | [Coupling geometry](coupling_geometry.md) |
| Which constants and reductions can be checked explicitly? | [Examples and verification](examples.md) |
| What does the result mean physically, and where does it stop applying? | [Interpretation and limits](interpretation.md) |
| Which parts are inherited, and which earlier models differ? | [Related work and attribution](../references/related_work.md) |

## The proof in one route

Start with the operational model, then read Sections 1–2 of the theorem for the exact finite construction. The coefficient bins determine complete even-size blocks and the discarded fraction. Each block uses a power-of-two subspace of its total-spin-zero sector.

Sections 3–4 derive two distinct bounds. The restricted-generator estimate controls a local channel in diamond norm. The sharper singlet-trace estimate controls decoded entanglement infidelity and is the input used by the outer code. Its full-singlet trace and the power-of-two restriction must be kept separate.

Sections 5–7 connect the blocks without assuming independent errors: exact non-signalling gives their marginals, Pauli twirling produces a correlated error distribution, and distance-code recovery bounds the final error by the expected Pauli weight. Section 8 supplies the size–rate–time limits, while Section 9 carefully separates deterministic existence at a prescribed duration from the keyed protocol's uniform time interval.

The symmetry proof is logically independent of achievability. It explains why the result concerns approximate finite-time storage despite a trivial stationary algebra. The resource page replaces the existential outer decoder in two explicit regimes and charges the retained classical key, calibration input, circuits, and boundary inaccuracies. The geometry corollary uses the same singlet trace argument for vector-valued couplings; its proof does not require the special commutation used in the scalar diamond-norm lemma.

## Distinctions that matter

- A scalar interaction commutant excludes exact noiseless storage at a fixed size. It does not give a size-independent mixing time.
- Marginal noise channels are exactly closed, but their errors remain correlated. The recovery proof retains those correlations.
- The block plots show entanglement infidelity. The full-memory guarantee is a half-diamond bound, including arbitrary entangled references.
- A good-code existence proof is separate from an efficient endpoint construction. Fixed-rate Tanner and growing-rate Reed–Solomon implementations have different parameter regimes.
- A reliable classical key is counted explicitly. No quantum system carries the payload outside the noisy register during storage.
- The common-field assumption is consequential: independent isotropic depolarization produces a constant-time ceiling.

[Repository entrypoint](../README.md) · [Exact theorem](storage_theorem.md) · [Reproduction instructions](../verification/README.md) · [Bibliography](../references/references.bib)
