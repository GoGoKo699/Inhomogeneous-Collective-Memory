#!/usr/bin/env python3
"""Deterministic finite-instance checks for Inhomogeneous-Collective-Memory.

These checks do not prove an asymptotic theorem or estimate an optimal lifetime.
No Monte Carlo sampling is used. Run from any directory; outputs are adjacent.
"""

from __future__ import annotations

import csv
import itertools
import json
import math
import platform
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.linalg import eigh, expm, null_space


HERE = Path(__file__).resolve().parent
DATA = HERE / "results"
FIGURES = HERE / "figures"
TOL = 2e-8
PAULI = {
    "I": np.eye(2, dtype=complex),
    "X": np.array([[0, 1], [1, 0]], dtype=complex),
    "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
    "Z": np.diag([1, -1]).astype(complex),
}


def kron_all(ops):
    out = np.array([[1.0]], dtype=complex)
    for op in ops:
        out = np.kron(out, op)
    return out


def pauli_word(word):
    return kron_all(PAULI[letter] for letter in word)


def collective(weights, axis):
    n = len(weights)
    return sum(w * pauli_word("I" * j + axis + "I" * (n - j - 1))
               for j, w in enumerate(weights))


def dissipator(jump):
    d = jump.shape[0]
    jj = jump.conj().T @ jump
    return (np.kron(jump.conj(), jump)
            - 0.5 * np.kron(np.eye(d), jj)
            - 0.5 * np.kron(jj.T, np.eye(d)))


def liouvillian(weights, rates=(1.0, 1.0)):
    return sum(rate * dissipator(collective(weights, axis))
               for axis, rate in zip("XZ", rates))


def vec(matrix):
    return np.asarray(matrix).reshape(-1, order="F")


def unvec(vector, rows, cols=None):
    return np.asarray(vector).reshape((rows, rows if cols is None else cols), order="F")


def singlet_four():
    """Explicit orthonormal four-spin singlets, qubit 0 most significant."""
    e = np.zeros((16, 2), dtype=complex)
    for bits, amplitude in {"0101": 0.5, "0110": -0.5,
                            "1001": -0.5, "1010": 0.5}.items():
        e[int(bits, 2), 0] = amplitude
    for bits, amplitude in {"0011": 1.0, "1100": 1.0,
                            "0101": -0.5, "0110": -0.5,
                            "1001": -0.5, "1010": -0.5}.items():
        e[int(bits, 2), 1] = amplitude / np.sqrt(3)
    return e


def decoder_data(e):
    """Inverse isometry on the code; fixed maximally mixed reset on leakage."""
    d, k = e.shape
    p = e @ e.conj().T
    q = np.eye(d) - p
    code = np.kron(e.T, e.conj().T)
    decoder = code + np.outer(vec(np.eye(k) / k), vec(q.T))
    complement = null_space(e.conj().T)
    kraus = [e.conj().T]
    for j in range(complement.shape[1]):
        for a in range(k):
            unit = np.eye(k)[:, a]
            kraus.append(np.outer(unit, complement[:, j].conj()) / np.sqrt(k))
    completeness = sum(v.conj().T @ v for v in kraus)
    kraus_super = sum(np.kron(v.conj(), v) for v in kraus)
    return decoder, code, q, {
        "kraus_count": len(kraus),
        "trace_preservation_residual": float(np.linalg.norm(completeness - np.eye(d))),
        "kraus_vs_direct_map_residual": float(np.linalg.norm(kraus_super - decoder)),
    }


def choi(superoperator, din=2, dout=2):
    result = np.zeros((din * dout, din * dout), dtype=complex)
    for j in range(din):
        for i in range(din):
            unit = np.zeros((din, din), dtype=complex)
            unit[i, j] = 1
            result += np.kron(unit, unvec(superoperator[:, i + j * din], dout)) / din
    return result


def channel_diagnostics(superoperator, din=2, dout=2):
    j = choi(superoperator, din, dout)
    reduced = np.trace(j.reshape(din, dout, din, dout), axis1=1, axis2=3)
    return {
        "choi_min_eigenvalue": float(eigh((j + j.conj().T) / 2, eigvals_only=True)[0]),
        "choi_hermiticity_residual": float(np.linalg.norm(j - j.conj().T)),
        "trace_preservation_residual": float(np.linalg.norm(reduced - np.eye(din) / din)),
    }


class ExactBlock:
    def __init__(self, weights, rates=(1.0, 1.0)):
        self.weights = np.asarray(weights, dtype=float)
        self.e = singlet_four()
        self.p = self.e @ self.e.conj().T
        self.encoder = np.kron(self.e.conj(), self.e)
        self.decoder, self.code_decoder, self.q, self.decoder_checks = decoder_data(self.e)
        self.generator = liouvillian(self.weights, rates)
        self.evals, self.evecs = eigh(self.generator)
        self.right = self.evecs.conj().T @ self.encoder
        self.left = self.decoder @ self.evecs
        self.code_left = self.code_decoder @ self.evecs
        self.leak_left = vec(self.q.T) @ self.evecs
        self.mixed_right = self.right @ vec(np.eye(2) / 2)
        self.gamma = sum(rates)
        self.center = float(np.mean(self.weights))
        self.d = float(np.sum(np.abs(self.weights - self.center)))
        self.trace_rate = sum(rate * np.trace(self.e.conj().T @ collective(self.weights, axis)
                                              @ collective(self.weights, axis) @ self.e).real / 2
                              for axis, rate in zip("XZ", rates))

    def at(self, time):
        factors = np.exp(time * self.evals)
        s = (self.left * factors[None, :]) @ self.right
        code_s = (self.code_left * factors[None, :]) @ self.right
        f_e = float(np.trace(s).real / 4)
        survival = float(np.trace(code_s).real / 4)
        leakage = float(np.dot(self.leak_left * factors, self.mixed_right).real)
        # Independent Bell-state evaluation of the same decoded fidelity.
        omega = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
        bell_fidelity = float(np.vdot(omega, choi(s) @ omega).real)
        assert abs(f_e - bell_fidelity) < TOL
        assert abs(f_e - survival - leakage / 4) < TOL
        diagnostics = channel_diagnostics(s)
        assert diagnostics["choi_min_eigenvalue"] > -TOL
        assert diagnostics["trace_preservation_residual"] < TOL
        assert 1 - f_e <= self.gamma * time * self.d**2 + TOL
        assert 1 - f_e <= self.trace_rate * time + TOL
        return s, {
            "time": float(time), "entanglement_fidelity": f_e,
            "infidelity": 1 - f_e, "leakage_probability": leakage,
            "encoded_bell_survival": survival,
            "operator_infidelity_bound": self.gamma * time * self.d**2,
            "trace_infidelity_bound": self.trace_rate * time,
            **diagnostics,
        }


def save_csv(name, rows):
    with (DATA / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def verify_blocks():
    e = singlet_four()
    annihilation = {axis: float(np.linalg.norm(collective(np.ones(4), axis) @ e))
                    for axis in "XYZ"}
    assert max(annihilation.values()) < TOL
    assert np.linalg.norm(e.conj().T @ e - np.eye(2)) < TOL
    uniform = ExactBlock(np.full(4, 1.3))
    _, uniform_result = uniform.at(4.0)
    assert abs(uniform_result["infidelity"]) < TOL
    rows, spectra, slopes = [], [], []
    selected_scaled_times = [0.0, 0.0025, 0.005, 0.01, 0.02, 0.03]
    grid = sorted(set(np.linspace(0, 0.03, 121).tolist() + selected_scaled_times))
    for n in [4, 8, 16, 32, 64]:
        indices = np.arange(n // 2 - 1, n // 2 + 3)
        weights = 1 + indices / n
        block = ExactBlock(weights)
        slope = -float(np.trace(block.decoder @ block.generator @ block.encoder).real / 4)
        # Full four-spin singlet and maximally mixed leakage reset give 10/n^2.
        assert abs(slope * n**2 - 10) < 1e-7
        assert abs(block.trace_rate * n**2 - 40 / 3) < 1e-7
        slopes.append({"register_size": n, "initial_infidelity_slope": slope,
                       "slope_times_n_squared": slope * n**2,
                       "encoded_bell_trace_rate_times_n_squared": float(block.trace_rate * n**2)})
        spectra.append({"register_size": n,
                        "generator_self_adjoint_residual": float(np.linalg.norm(block.generator - block.generator.conj().T)),
                        "largest_generator_eigenvalue": float(block.evals[-1]),
                        "smallest_generator_eigenvalue": float(block.evals[0])})
        for tau in grid:
            _, result = block.at(tau * n**2)
            rows.append({"register_size": n, "simulated_block_spins": 4,
                         "first_site_index": int(indices[0]), "last_site_index": int(indices[-1]),
                         "g_min": float(weights[0]), "g_max": float(weights[-1]),
                         "scaled_time_t_over_n_squared": float(tau), **result})
    save_csv("block_dynamics.csv", rows)
    selected = [row for row in rows if any(abs(row["scaled_time_t_over_n_squared"] - t) < 1e-12
                                          for t in selected_scaled_times)]
    save_csv("block_selected_times.csv", selected)
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.1), layout="constrained")
    colors = plt.cm.viridis(np.linspace(0.08, 0.88, 5))
    for color, n in zip(colors, [4, 8, 16, 32, 64]):
        subset = [r for r in rows if r["register_size"] == n]
        positive = [r for r in subset if r["time"] > 0]
        axes[0].plot([r["time"] for r in positive], [r["infidelity"] for r in positive],
                     label=f"n = {n}", color=color)
        axes[1].plot([r["scaled_time_t_over_n_squared"] for r in subset],
                     [r["infidelity"] for r in subset], label=f"n = {n}", color=color)
    axes[0].set_xscale("log")
    axes[0].set_xlabel("Physical storage time t")
    axes[0].set_ylabel("Decoded block entanglement infidelity")
    axes[0].set_title("One exact four-spin marginal per register size")
    tau = np.linspace(0, 0.03, 121)
    axes[1].plot(tau, (40 / 3) * tau, "--", color="#9d2636", linewidth=1.8,
                 label="Trace bound (40/3)t/n²")
    axes[1].plot(tau, 32 * tau, ":", color="#67717e", linewidth=1.6,
                 label="Operator bound 32t/n²")
    axes[1].set_xlabel("Rescaled time t/n²")
    axes[1].set_title("Comparison with the block bound")
    for ax in axes:
        ax.grid(alpha=0.2)
        ax.set_ylim(-0.005, 1.0)
    axes[0].set_ylim(-0.005, 0.4)
    axes[0].legend(frameon=False, fontsize=8, loc="upper left")
    axes[1].legend(frameon=False, fontsize=8, loc="upper left")
    fig.savefig(FIGURES / "block_fidelity_scaling.png", dpi=190)
    fig.savefig(FIGURES / "block_fidelity_scaling.pdf")
    plt.close(fig)
    return {
        "singlet_annihilation_residuals": annihilation,
        "decoder": uniform.decoder_checks,
        "uniform_coupling_control_infidelity_at_t4": uniform_result["infidelity"],
        "grid_points": len(rows), "spectra": spectra, "initial_slopes": slopes,
        "largest_operator_bound_excess": max(r["infidelity"] - r["operator_infidelity_bound"] for r in rows),
        "largest_trace_bound_excess": max(r["infidelity"] - r["trace_infidelity_bound"] for r in rows),
        "smallest_logical_choi_eigenvalue": min(r["choi_min_eigenvalue"] for r in rows),
        "largest_logical_trace_preservation_residual": max(r["trace_preservation_residual"] for r in rows),
    }


def verify_singlet_trace_variance():
    """Check the full trace formula and the worst chosen power-of-two subspace."""
    reports, vector_reports = [], []
    for m in [4, 6, 8]:
        js = [collective(np.ones(m), axis) for axis in "XYZ"]
        spin_squared = sum(j @ j for j in js)
        eig, basis = eigh(spin_squared)
        singlets = basis[:, eig < 1e-9]
        dimension = math.comb(m, m // 2) // (m // 2 + 1)
        assert singlets.shape[1] == dimension
        logical_dimension = 1 << (dimension.bit_length() - 1)
        weights = 1 + np.arange(1, m + 1) / 32
        compressed = {}
        for axis in "XYZ":
            a = collective(weights, axis)
            compressed[axis] = singlets.conj().T @ a @ a @ singlets
        formula = (m / (m - 1)) * float(np.sum((weights - np.mean(weights))**2))
        full_average = float(np.trace(compressed["Z"]).real / dimension)
        values, vectors = eigh(compressed["Z"])
        # This selected subspace maximizes the trace among subspaces of this size.
        chosen = vectors[:, -logical_dimension:]
        chosen_average = float(np.trace(chosen.conj().T @ compressed["Z"] @ chosen).real / logical_dimension)
        rho = dimension / logical_dimension
        axis_residual = max(float(np.linalg.norm(compressed[axis] - compressed["Z"])) for axis in "XY")
        assert abs(full_average - formula) < TOL
        assert chosen_average <= rho * formula + TOL
        assert axis_residual < TOL
        reports.append({"block_size": m, "singlet_dimension": dimension,
                        "chosen_logical_dimension": logical_dimension, "dimension_ratio_rho": rho,
                        "full_singlet_trace_variance": full_average, "analytic_trace_variance": formula,
                        "worst_selected_subspace_trace_variance": chosen_average,
                        "rho_times_full_trace_bound": rho * formula,
                        "compressed_axis_equality_residual": axis_residual})
        if m in [4, 6]:
            coordinate = (np.arange(1, m + 1) - (m + 1) / 2) / m
            vectors_at_sites = np.column_stack([1 + .3 * coordinate,
                                                .25 + .2 * coordinate**2,
                                                -.15 + .4 * coordinate])
            vector_mean = np.mean(vectors_at_sites, axis=0)
            a = sum(collective(vectors_at_sites[:, index], axis)
                    for index, axis in enumerate("XYZ"))
            b = sum(collective(np.full(m, vector_mean[index]), axis)
                    for index, axis in enumerate("XYZ"))
            d = a - b
            compressed_vector = singlets.conj().T @ a @ a @ singlets
            vector_formula = (m / (m - 1)) * float(np.sum((vectors_at_sites - vector_mean)**2))
            vector_average = float(np.trace(compressed_vector).real / dimension)
            eigenvalues = eigh(compressed_vector, eigvals_only=True)
            worst_vector_average = float(np.mean(eigenvalues[-logical_dimension:]))
            commutator = float(np.linalg.norm(b @ d - d @ b))
            uncompressed_square_difference = float(np.linalg.norm((a @ a - d @ d) @ singlets))
            compressed_square_residual = float(np.linalg.norm(compressed_vector - singlets.conj().T @ d @ d @ singlets))
            first_moment_residual = float(np.linalg.norm(singlets.conj().T @ a @ singlets))
            assert abs(vector_average - vector_formula) < TOL
            assert worst_vector_average <= rho * vector_formula + TOL
            assert max(compressed_square_residual, first_moment_residual) < TOL
            assert commutator > 1e-3 and uncompressed_square_difference > 1e-3
            vector_reports.append({"block_size": m, "vectors_at_sites": vectors_at_sites.tolist(),
                                   "full_singlet_trace_variance": vector_average,
                                   "analytic_vector_trace_variance": vector_formula,
                                   "worst_selected_subspace_trace_variance": worst_vector_average,
                                   "rho_times_full_trace_bound": rho * vector_formula,
                                   "B_D_commutator_norm": commutator,
                                   "uncompressed_A_squared_vs_D_squared_residual": uncompressed_square_difference,
                                   "compressed_A_squared_vs_D_squared_residual": compressed_square_residual,
                                   "compressed_first_moment_residual": first_moment_residual})
    return {"cases": reports, "vector_coefficient_cases": vector_reports,
            "selected_subspace_rule": "largest eigenvalues of the compressed squared jump"}


def partial_trace_b(matrix, da, db):
    return np.trace(matrix.reshape(da, db, da, db), axis1=1, axis2=3)


def partial_trace_matrix(da, db):
    d = da * db
    out = np.zeros((da * da, d * d), dtype=complex)
    for j in range(d):
        for i in range(d):
            basis = np.zeros((d, d), dtype=complex)
            basis[i, j] = 1
            out[:, i + j * d] = vec(partial_trace_b(basis, da, db))
    return out


def verify_nonsignalling():
    weights = np.array([1.125, 1.375, 1.625, 1.875])
    rates = (1.0, 0.7)
    trace_b = partial_trace_matrix(4, 4)
    full = liouvillian(weights, rates)
    local = liouvillian(weights[:2], rates)
    residual = float(np.linalg.norm(trace_b @ full - local @ trace_b))
    cross_residuals = {}
    for axis in "XZ":
        a = np.kron(collective(weights[:2], axis), np.eye(4))
        b = np.kron(np.eye(4), collective(weights[2:], axis))
        cross = dissipator(a + b) - dissipator(a) - dissipator(b)
        cross_residuals[axis] = float(np.linalg.norm(trace_b @ cross))
    amplitudes = np.sqrt([0.5, 0.3, 0.15, 0.05]) * np.exp(1j * np.array([0, .3, .8, 1.7]))
    state = vec(np.diag(amplitudes))
    rho = np.outer(state, state.conj())
    time = 0.37
    evolved = unvec(expm(time * full) @ vec(rho), 16)
    reduced = partial_trace_b(rho, 4, 4)
    evolved_local = unvec(expm(time * local) @ vec(reduced), 4)
    finite_time_residual = float(np.linalg.norm(partial_trace_b(evolved, 4, 4) - evolved_local))
    assert max([residual, finite_time_residual, *cross_residuals.values()]) < TOL
    return {"full_operator_space_intertwining_residual": residual,
            "traced_cross_dissipator_residuals": cross_residuals,
            "correlated_input_finite_time_residual": finite_time_residual,
            "finite_time": time, "operator_space_dimension_checked": 256}


def ptm_from_super(superoperator):
    basis = list(PAULI.values())
    return np.array([[np.trace(a @ unvec(superoperator @ vec(b), 2)).real / 2
                      for b in basis] for a in basis])


def pauli_commutation_sign(a, b):
    mismatches = sum(x != "I" and y != "I" and x != y for x, y in zip(a, b))
    return -1 if mismatches % 2 else 1


def verify_correlated_twirl():
    e = singlet_four()
    decoder, _, _, _ = decoder_data(e)
    encoder = np.kron(e.conj(), e)
    weights = 1 + np.arange(1, 9) / 8
    # A specified diagnostic mixture, not a Brownian simulation or fitted sample.
    paths = [(0.65, 0.0, 0.0), (0.20, 0.9, -0.6), (0.15, 2.1, 1.3)]
    one_labels = list(PAULI)
    one_signs = np.array([[pauli_commutation_sign(a, b) for b in one_labels] for a in one_labels])
    labels = ["".join(x) for x in itertools.product("IXYZ", repeat=2)]
    signs = np.array([[pauli_commutation_sign(a, b) for b in labels] for a in labels])
    global_ptm = np.zeros((16, 16))
    expected_law = np.zeros(16)
    paths_report = []
    for probability, theta_x, theta_z in paths:
        block_ptms, block_laws = [], []
        for block in range(2):
            units = [expm(-1j * theta_z * g * PAULI["Z"]) @ expm(-1j * theta_x * g * PAULI["X"])
                     for g in weights[4 * block:4 * block + 4]]
            unitary = kron_all(units)
            logical = decoder @ np.kron(unitary.conj(), unitary) @ encoder
            ptm = ptm_from_super(logical)
            law = one_signs @ np.diag(ptm) / 4
            assert min(law) > -TOL
            block_ptms.append(ptm)
            block_laws.append(law)
        global_ptm += probability * np.kron(*block_ptms)
        expected_law += probability * np.kron(*block_laws)
        paths_report.append({"probability": probability, "theta_x": theta_x, "theta_z": theta_z,
                             "block_nonidentity_probabilities": [float(1 - p[0]) for p in block_laws]})
    twirled = sum(sign[:, None] * global_ptm * sign[None, :] for sign in signs) / 16
    direct_law = signs @ np.diag(twirled) / 16
    off_diagonal = twirled - np.diag(np.diag(twirled))
    law_residual = float(np.linalg.norm(direct_law - expected_law))
    assert np.linalg.norm(off_diagonal) < TOL and law_residual < TOL
    assert min(direct_law) > -TOL and abs(sum(direct_law) - 1) < TOL
    p1 = sum(p for label, p in zip(labels, direct_law) if label[0] != "I")
    p2 = sum(p for label, p in zip(labels, direct_law) if label[1] != "I")
    joint = sum(p for label, p in zip(labels, direct_law) if "I" not in label)
    covariance = joint - p1 * p2
    assert covariance > 1e-5  # This diagnostic actually contains correlated errors.
    save_csv("correlated_twirl_pauli_law.csv", [{"pauli": label, "probability": float(p),
                                                "weight": sum(c != "I" for c in label)}
                                               for label, p in zip(labels, direct_law)])
    return {"ensemble_type": "specified finite diagnostic ensemble; no sampling",
            "paths": paths_report,
            "untwirled_off_diagonal_ptm_norm": float(np.linalg.norm(global_ptm - np.diag(np.diag(global_ptm)))),
            "twirled_off_diagonal_ptm_norm": float(np.linalg.norm(off_diagonal)),
            "conditional_product_vs_direct_twirl_law_residual": law_residual,
            "block_nonidentity_probabilities": [float(p1), float(p2)],
            "both_nonidentity_probability": float(joint),
            "nonidentity_indicator_covariance": float(covariance)}


def verify_five_qubit_recovery():
    stabilizer_words = ["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"]
    stabilizers = [pauli_word(s) for s in stabilizer_words]
    identity = np.eye(32)
    projector = identity.astype(complex)
    for stabilizer in stabilizers:
        projector = projector @ (identity + stabilizer) / 2
    zero = projector[:, 0] / np.linalg.norm(projector[:, 0])
    e = np.column_stack([zero, pauli_word("XXXXX") @ zero])
    assert np.linalg.norm(e.conj().T @ e - np.eye(2)) < TOL
    singles = ["IIIII"] + ["I" * site + axis + "I" * (4 - site)
                              for site in range(5) for axis in "XYZ"]

    def syndrome(word):
        return tuple(int(pauli_commutation_sign(word, s) == -1) for s in stabilizer_words)

    correction = {syndrome(word): word for word in singles}
    assert len(correction) == 16
    recovery_kraus = []
    for syn, word in correction.items():
        ps = identity.astype(complex)
        for bit, stabilizer in zip(syn, stabilizers):
            ps = ps @ (identity + (-1) ** bit * stabilizer) / 2
        recovery_kraus.append(e.conj().T @ pauli_word(word) @ ps)
    recovery_tp = float(np.linalg.norm(sum(k.conj().T @ k for k in recovery_kraus) - identity))
    assert recovery_tp < TOL
    rows, logical_labels = [], {}
    for letters in itertools.product("IXYZ", repeat=5):
        word = "".join(letters)
        syn = syndrome(word)
        logical = e.conj().T @ pauli_word(correction[syn]) @ pauli_word(word) @ e
        overlaps = {label: np.trace(p.conj().T @ logical) / 2 for label, p in PAULI.items()}
        result = max(overlaps, key=lambda k: abs(overlaps[k]))
        residual = float(np.linalg.norm(logical - overlaps[result] * PAULI[result]))
        assert abs(abs(overlaps[result]) - 1) < TOL and residual < TOL
        weight = sum(letter != "I" for letter in word)
        if weight <= 1:
            assert result == "I"
        logical_labels[word] = result
        rows.append({"physical_pauli": word, "weight": weight,
                     "syndrome": "".join(map(str, syn)), "recovery_pauli": correction[syn],
                     "residual_logical_pauli": result, "matrix_residual": residual})
    save_csv("five_qubit_all_paulis.csv", rows)
    laws = {
        "perfectly_correlated_five_site_burst": {"IIIII": .98, "XXXXX": .02},
        "single_errors_plus_correlated_bursts": {
            "IIIII": .94, "ZIIII": .006, "IZIII": .006, "IIZII": .006,
            "IIIZI": .006, "IIIIZ": .006, "XXIII": .02, "XXXXX": .01},
    }
    reports = []
    for name, law in laws.items():
        assert abs(sum(law.values()) - 1) < TOL
        logical_law = {label: 0.0 for label in PAULI}
        marginals = np.zeros(5)
        expected_weight, high_weight_probability = 0.0, 0.0
        for word, probability in law.items():
            logical_law[logical_labels[word]] += probability
            mask = np.array([letter != "I" for letter in word])
            marginals += probability * mask
            expected_weight += probability * sum(mask)
            high_weight_probability += probability * (sum(mask) > 1)
        logical_super = sum(probability * np.kron(PAULI[label].conj(), PAULI[label])
                            for label, probability in logical_law.items())
        bell_distance = float(sum(abs(eigh(choi(logical_super) - choi(np.eye(4)), eigvals_only=True))) / 2)
        exact_half_diamond = 1 - logical_law["I"]
        assert abs(bell_distance - exact_half_diamond) < TOL
        assert exact_half_diamond <= high_weight_probability + TOL
        assert high_weight_probability <= expected_weight / 2 + TOL
        assert expected_weight <= 5 * max(marginals) + TOL
        reports.append({"name": name, "physical_law": law, "logical_law_after_recovery": logical_law,
                        "physical_site_error_marginals": marginals.tolist(),
                        "expected_error_weight": float(expected_weight),
                        "probability_weight_above_one": float(high_weight_probability),
                        "exact_logical_half_diamond_error": exact_half_diamond,
                        "bell_input_trace_distance": bell_distance,
                        "markov_bound_from_expected_weight": float(min(1, expected_weight)),
                        "integer_markov_bound_from_expected_weight": float(min(1, expected_weight / 2)),
                        "p_max_over_q_bound_q_equals_one_fifth": float(min(1, 5 * max(marginals)))})
    return {"code": "[[5,1,3]] with perfect final syndrome recovery",
            "paulis_exhaustively_checked": len(rows), "single_site_correctable_paulis": 16,
            "recovery_trace_preservation_residual": recovery_tp,
            "largest_logical_pauli_classification_residual": max(r["matrix_residual"] for r in rows),
            "designed_correlated_laws": reports}


def verify_depolarization_boundary():
    eta = 0.4
    collective_generator = liouvillian([1.1, 1.9], rates=(1.0, 0.7))
    independent = sum((eta / 4) * dissipator(pauli_word("I" * site + axis + "I" * (1 - site)))
                      for site in range(2) for axis in "XYZ")
    commutator_residual = float(np.linalg.norm(independent @ collective_generator - collective_generator @ independent))
    assert commutator_residual < TOL
    rows = []
    for dimensionless_time in [0.0, .5 * np.log(3), np.log(3), 2 * np.log(3)]:
        contraction = np.exp(-dimensionless_time)
        dep = contraction * np.eye(4) + (1 - contraction) * np.outer(vec(np.eye(2) / 2), vec(np.eye(2)))
        j = choi(dep)
        partial_transpose = j.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)
        min_eigenvalue = float(eigh(partial_transpose, eigvals_only=True)[0])
        formula = (1 - 3 * contraction) / 4
        assert abs(min_eigenvalue - formula) < TOL
        rows.append({"eta_t": float(dimensionless_time), "bloch_contraction": float(contraction),
                     "partial_transpose_min_eigenvalue": min_eigenvalue,
                     "analytic_partial_transpose_min_eigenvalue": float(formula)})
    # Explicit measure-and-prepare realization at contraction 1/3.
    prepare = np.zeros((4, 4), dtype=complex)
    for axis in "XYZ":
        for sign in [-1, 1]:
            state = (PAULI["I"] + sign * PAULI[axis]) / 2
            prepare += np.outer(vec(state), vec((state / 3).T))
    expected = np.eye(4) / 3 + (2 / 3) * np.outer(vec(np.eye(2) / 2), vec(np.eye(2)))
    measure_prepare_residual = float(np.linalg.norm(prepare - expected))
    assert measure_prepare_residual < TOL
    return {"independent_rate_eta": eta,
            "two_spin_generator_commutator_residual": commutator_residual,
            "entanglement_breaking_time": float(np.log(3) / eta),
            "threshold_measure_prepare_residual": measure_prepare_residual,
            "choi_partial_transpose_checks": rows}


def verify_calibration():
    rows = []
    for n in [16, 32, 64]:
        estimates = 1 + np.arange(n // 2 - 1, n // 2 + 3) / n
        for label, eta in [("zero", 0.0), ("one_over_n", 1 / n), ("fixed_0.01", .01)]:
            actual = estimates + eta * np.array([-1, -1, 1, 1])
            block = ExactBlock(actual)
            _, result = block.at(.005 * n**2)
            coarse_d = 4 * ((estimates[-1] - estimates[0]) / 2 + eta)
            calibration_bound = 2 * result["time"] * coarse_d**2
            calibration_trace_bound = calibration_bound / 3
            assert block.d <= coarse_d + TOL
            assert result["infidelity"] <= calibration_bound + TOL
            assert result["infidelity"] <= calibration_trace_bound + TOL
            rows.append({"register_size": n, "calibration_case": label,
                         "eta": eta, "time": result["time"],
                         "infidelity": result["infidelity"],
                         "exact_block_spread_d": block.d,
                         "operator_bound_from_actual_coefficients": result["operator_infidelity_bound"],
                         "trace_bound_from_actual_coefficients": result["trace_infidelity_bound"],
                         "operator_bound_from_calibration_envelope": calibration_bound,
                         "trace_bound_from_calibration_envelope": calibration_trace_bound})
    save_csv("calibration_examples.csv", rows)
    return {"cases": len(rows), "description": "deterministic perturbations aligned with the estimated block spread"}


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    summary = {
        "status": "all deterministic assertions passed",
        "evidence_type": "finite-dimensional deterministic numerical checks plus exact Pauli enumeration; no Monte Carlo",
        "tolerance": TOL,
        "environment": {"python": platform.python_version(), "numpy": np.__version__,
                        "scipy": scipy.__version__, "matplotlib": matplotlib.__version__},
    }
    for name, check in [("inner_blocks", verify_blocks), ("singlet_trace_variance", verify_singlet_trace_variance),
                        ("nonsignalling", verify_nonsignalling),
                        ("correlated_twirl", verify_correlated_twirl),
                        ("outer_recovery", verify_five_qubit_recovery),
                        ("depolarization_boundary", verify_depolarization_boundary),
                        ("calibration", verify_calibration)]:
        print(f"Running {name} ...", flush=True)
        summary[name] = check()
    (DATA / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "results": str(DATA), "figures": str(FIGURES)}, indent=2))


if __name__ == "__main__":
    main()
