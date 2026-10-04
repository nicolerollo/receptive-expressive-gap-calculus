"""Developmental models used in the MATH 140 project.

The final paper is authoritative.

Provenance
----------
Down syndrome (DS):
    Slopes were estimated by the project author from Figure 2 of
    D'Souza et al. (2026). Intercepts were derived by anchoring those
    slopes to the published Time 1 group means in Table 2 at mean
    chronological age 27.81 months. The resulting intercepts are rounded
    to three decimals because those rounded DS equations are the models
    used in the final paper and its Python appendices.

Fragile X syndrome (FXS):
    Ordinary least squares is recomputed from the seven published
    age-cluster means reported in Table II of Roberts et al. (2009),
    using the nominal cluster ages as t-values. Unrounded regression
    coefficients are retained for calculations, matching the final paper.

These are group-level mathematical models, not individual predictions.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"


@dataclass(frozen=True)
class LinearModel:
    """A linear developmental trajectory y(t) = slope * t + intercept."""

    slope: float
    intercept: float

    def value(self, t):
        return self.slope * np.asarray(t) + self.intercept

    def inverse(self, score: float) -> float:
        """Chronological age at which the trajectory reaches a numerical score."""
        return (score - self.intercept) / self.slope

    @property
    def derivative(self) -> float:
        return self.slope


def load_ds_models() -> dict[str, LinearModel]:
    """Construct the final-paper DS models from their documented inputs."""
    rows: dict[str, dict[str, str]] = {}

    with (DATA_DIR / "ds_model_inputs.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows[row["trajectory"]] = row

    models: dict[str, LinearModel] = {}

    for trajectory in ("receptive", "expressive"):
        row = rows[trajectory]
        slope = float(row["estimated_slope"])
        anchor_ca = float(row["anchor_ca_months"])
        anchor_ae = float(row["anchor_ae_months"])
        round_decimals = int(row["intercept_round_decimals"])

        raw_intercept = anchor_ae - slope * anchor_ca

        # The final paper and appendices use the rounded DS equations.
        intercept = round(raw_intercept, round_decimals)

        models[trajectory] = LinearModel(slope=slope, intercept=intercept)

    return models


def load_fxs_models() -> dict[str, LinearModel]:
    """Fit the FXS models by OLS from the seven published aggregate means."""
    ages = []
    receptive = []
    expressive = []

    with (DATA_DIR / "fxs_roberts2009_tableII.csv").open(
        newline="", encoding="utf-8"
    ) as f:
        for row in csv.DictReader(f):
            ages.append(float(row["nominal_cluster_age_months"]))
            receptive.append(float(row["receptive_ae_mean_months"]))
            expressive.append(float(row["expressive_ae_mean_months"]))

    ages = np.asarray(ages, dtype=float)
    receptive = np.asarray(receptive, dtype=float)
    expressive = np.asarray(expressive, dtype=float)

    m_r, b_r = np.polyfit(ages, receptive, 1)
    m_e, b_e = np.polyfit(ages, expressive, 1)

    return {
        "receptive": LinearModel(float(m_r), float(b_r)),
        "expressive": LinearModel(float(m_e), float(b_e)),
    }


def gap_coefficients(
    receptive: LinearModel, expressive: LinearModel
) -> tuple[float, float]:
    """Return slope and intercept of G(t) = R(t) - E(t)."""
    return (
        receptive.slope - expressive.slope,
        receptive.intercept - expressive.intercept,
    )


def proportional_gap(t, receptive: LinearModel, expressive: LinearModel):
    """Q(t) = R(t) / E(t)."""
    return receptive.value(t) / expressive.value(t)


def proportional_gap_derivative_numerator(
    receptive: LinearModel, expressive: LinearModel
) -> float:
    """Constant numerator of Q'(t) for two linear trajectories."""
    return (
        receptive.slope * expressive.intercept
        - receptive.intercept * expressive.slope
    )


def score_gap(t, receptive: LinearModel, expressive: LinearModel):
    """G(t) = R(t) - E(t)."""
    return receptive.value(t) - expressive.value(t)


def time_gap(score: float, receptive: LinearModel, expressive: LinearModel) -> float:
    """H(A) = t_E(A) - t_R(A)."""
    return expressive.inverse(score) - receptive.inverse(score)
