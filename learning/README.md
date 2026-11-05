# Learning the storage theorem

The central question is how an unknown quantum state can survive correlated noise even when the finite register has no exact noiseless subsystem. This route develops the answer from one-spin channels and encoded blocks to the complete storage guarantee, its endpoint resources, and its physical limits.

The shared map contains **30 milestones**, with **12 background/preliminary milestones** and **18 narrative/innovation milestones**. It describes the scientific dependencies for every reader. The tutorial develops those targets as one continuous account in eight contiguous groups.

## The connected route

| Purpose | Page | What it supplies |
|---|---|---|
| See the questions and their dependencies | [Thirty-milestone map](milestones.md) | M01–M30, their understanding targets, conceptual connections, and source pointers |
| Connect the textbook foundation to the result | [Selected anchor and bridge](anchor_bridge.md) | The sole educational anchor, verified section pointers, notation conventions, and the additional proof steps |
| Follow the argument with a concrete memory | [Continuous tutorial](tutorial.md) | The complete milestone sequence, including an analytic twenty-spin example |
| Inspect exact statements and proofs | [Scientific overview](../science/README.md) | The authoritative model, finite theorem, symmetry argument, implementation bounds, and extensions |
| Check the evidence and inherited ingredients | [Verification](../verification/README.md) and [related work](../references/related_work.md) | Reproduction commands, the scope of finite checks, and primary-source attribution |

The **single educational anchor** is Michael A. Nielsen and Isaac L. Chuang, *Quantum Computation and Quantum Information*, **10th Anniversary Edition**. Its channel, fidelity and error-correction foundations support the project. The [bridge](anchor_bridge.md) identifies precisely where the singlet, semigroup, reference-uniform and correlated-error arguments are supplied locally.

## A complete small memory

The tutorial's worked example uses twenty spins with supplied couplings $`g_j=1+j/20`$ and noise rates $`\gamma_x=\gamma_z=1`$. Five four-spin singlet blocks each carry one inner logical qubit. An outer $`[[5,1,3]]`$ code then stores one final logical qubit, giving rate $`1/20`$, with **ten retained classical Pauli-key bits**.

The analytic recovery bound gives half-diamond error at most $`1/30`$ throughout $`0\le t\le0.4`$, including an arbitrary entangled reference. The common-field correlations remain present, and all correction occurs at the endpoint. This example connects the physical carrier, encoded dimensions, key cost, local fidelity estimate and final recovery in one protocol. Its [full derivation](tutorial.md) uses the explicit five-qubit code with the [block and recovery bounds](../science/storage_theorem.md#6-global-pauli-twirling-and-correlated-error-correction); the finite Gilbert–Varshamov count is not invoked for this small example.

## Reading the guarantees

The [finite theorem](../science/storage_theorem.md) gives the precise quantifiers and roundings. Its fixed-rate quadratic interval, existential rate-one subquadratic limit, and the [polynomial endpoint constructions](../science/resources.md) are distinct guarantees. The learning route preserves those distinctions, together with supplied calibration, reliable classical storage, ideal endpoint assumptions and the open question of optimal lifetime.

[Repository entrypoint](../README.md) · [Scientific overview](../science/README.md) · [Model](../science/model.md) · [Interpretation](../science/interpretation.md)
