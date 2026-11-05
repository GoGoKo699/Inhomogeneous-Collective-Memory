# Deterministic verification

This directory checks concrete failure modes in the memory argument: leakage decoding, normalization of the inner error bound, spectator correlations, Pauli twirling, correction under correlated errors, and the independent-noise boundary. The checks use exact finite matrices evaluated in floating point and exhaustive Pauli enumeration. They contain no Monte Carlo sampling and do not establish asymptotic optimality.

## Reproduce

From the repository root, run:

```bash
python -m pip install -r requirements.txt
python verification/verify_memory.py
```

The script requires NumPy, SciPy, and Matplotlib. It records the versions used in [results/summary.json](results/summary.json). The recorded run used Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, and Matplotlib 3.10.8. The assertion tolerance is $`2\times10^{-8}`$; the largest recorded logical-channel trace-preservation residual is approximately $`1.2\times10^{-12}`$.

The script overwrites its generated results and figures. It does not download data, use network access, or modify source files. All physical coefficients, diagnostic noise ensembles, and Pauli distributions are specified in the source. The largest physical density-matrix evolution is a four-spin system with Hilbert-space dimension 16. The eight-spin trace-variance check uses a 256-dimensional spin matrix, not a 65,536-dimensional Liouvillian.

## What is checked

| Check | Concrete risk addressed | Evidence |
|---|---|---|
| Four-spin singlet decoder | Leakage replacement might fail complete positivity or trace preservation | Explicit 29-Kraus representation agrees with the direct decoder; Kraus completeness residual below $`1.4\times10^{-15}`$ |
| Exact block semigroups | A rate, factor-of-two, or reference normalization error might invalidate the bound | 605 size/time points; Choi positivity and trace preservation; Bell-state and superoperator fidelity agree; exact initial slope $`10/n^2`$ |
| Full-singlet and selected-subspace trace variance | Restricting the Catalan dimension or allowing nonparallel local vectors might invalidate the mean error bound | Scalar formula at $`m=4,6,8`$; vector formula at $`m=4,6`$; deliberately highest-variance subspaces; nonzero $`[B,D]`$ verified |
| Non-signalling | Cross dissipator terms or initially correlated spectators might change a block's channel | Intertwining identity checked on the entire 256-dimensional operator space, plus a finite-time correlated input |
| Correlated two-block twirl | Pauli randomization might incorrectly assume independent noise | Direct twirl agrees with a conditional product decomposition; the resulting error indicators have nonzero covariance |
| Five-qubit recovery | A marginal error estimate might not control reference-entangled inputs under correlated bursts | All 1,024 physical Pauli errors classified; all 16 correctable errors corrected; two correlated laws checked against both the integer Markov bound and the looser $`p/q`$ bound |
| Independent depolarization | The claimed constant-time ceiling might use a noncommuting factorization | Generator commutation, Choi partial-transpose threshold, and an explicit measure-and-prepare representation checked |
| Calibration | Using estimated coefficients might silently preserve an unjustified spacing bound | Nine deterministic perturbation cases, with actual-coefficient and calibration-envelope bounds recorded separately |

The singlet-trace test searches the highest-variance subspace of the required dimension by diagonalizing the compressed positive operator. It does not choose a particularly favorable subspace to make the estimate pass.

## Generated files

- [results/summary.json](results/summary.json): residuals, parameters, software versions, and aggregate results.
- [results/block_dynamics.csv](results/block_dynamics.csv): every computed point underlying the plot, including both analytic bounds, leakage, and Choi diagnostics.
- [results/block_selected_times.csv](results/block_selected_times.csv): the six selected rescaled times for each register size.
- [results/correlated_twirl_pauli_law.csv](results/correlated_twirl_pauli_law.csv): the complete two-qubit Pauli law after twirling.
- [results/five_qubit_all_paulis.csv](results/five_qubit_all_paulis.csv): exhaustive syndrome, correction, and residual logical Pauli for all 1,024 physical Paulis.
- [results/calibration_examples.csv](results/calibration_examples.csv): actual errors and bounds for specified coefficient perturbations.
- [figures/block_fidelity_scaling.png](figures/block_fidelity_scaling.png) and [figures/block_fidelity_scaling.pdf](figures/block_fidelity_scaling.pdf): the exact block calculation and its rescaling.

## Evidence interpretation

Here $`n`$ is the total register size entering the profile $`g_j=1+j/n`$. Each plotted calculation evolves one four-spin marginal near the register midpoint. This is legitimate because the block marginal follows its own exact semigroup, including for correlated global inputs; that identity is checked independently. A curve labeled $`n=64`$ is therefore not a 64-spin numerical evolution.

The two-block diagnostic uses a specified finite mixture of common rotations. Its probabilities are inputs to an algebraic check, not measured or fitted Brownian probabilities. The five-qubit test likewise uses specified correlated Pauli distributions. These calculations verify the coding reduction for correlations; they do not estimate the full memory's physical failure distribution.

For a logical Pauli channel the half-diamond error from identity equals the total nonidentity probability. The five-qubit test can therefore compare an exact diamond error with the theorem's Markov bound without solving a numerical semidefinite program. Inner-block entanglement infidelity in the plot is a different metric and is labeled accordingly.

Analytic examples, conventions, and the independent-noise ceiling are developed in [science/examples.md](../science/examples.md).

## GitHub mathematical rendering

The separate [hosted mathematics collector](github_math/references/hosted-rendering.md) checks actual commit-pinned GitHub pages at two viewport widths. It compares every inventoried expression with captured mathematical structure and saves screenshots for visual review. The pull-request workflow runs with read-only repository permissions. This presentation check is separate from the scientific assertions and finite-matrix evidence above.
