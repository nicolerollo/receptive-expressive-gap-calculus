"""Regression tests for the calculations reported in the final paper."""

from __future__ import annotations

import csv
import math
from pathlib import Path
import sys
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from models import (  # noqa: E402
    gap_coefficients,
    load_ds_models,
    load_fxs_models,
    proportional_gap,
    proportional_gap_derivative_numerator,
    score_gap,
    time_gap,
)


class ReproductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ds = load_ds_models()
        cls.fxs = load_fxs_models()

    def test_ds_anchor_construction_reproduces_final_paper_equations(self):
        """Published Table 2 anchors + estimated slopes reproduce the paper models."""
        rows = {}
        with (REPO_ROOT / "data" / "ds_model_inputs.csv").open(
            newline="", encoding="utf-8"
        ) as f:
            for row in csv.DictReader(f):
                rows[row["trajectory"]] = row

        for trajectory, expected_intercept in (
            ("receptive", 2.176),
            ("expressive", 4.904),
        ):
            row = rows[trajectory]
            slope = float(row["estimated_slope"])
            anchor_ca = float(row["anchor_ca_months"])
            anchor_ae = float(row["anchor_ae_months"])
            raw_intercept = anchor_ae - slope * anchor_ca
            rounded_intercept = round(
                raw_intercept, int(row["intercept_round_decimals"])
            )
            self.assertEqual(rounded_intercept, expected_intercept)

    def test_final_paper_ds_models(self):
        self.assertEqual(self.ds["receptive"].slope, 0.48845)
        self.assertEqual(self.ds["receptive"].intercept, 2.176)
        self.assertEqual(self.ds["expressive"].slope, 0.33714)
        self.assertEqual(self.ds["expressive"].intercept, 4.904)

    def test_fxs_ols_coefficients(self):
        """OLS is recomputed from Roberts et al. Table II aggregate means."""
        self.assertAlmostEqual(
            self.fxs["receptive"].slope,
            0.4497724620770128,
            places=13,
        )
        self.assertAlmostEqual(
            self.fxs["receptive"].intercept,
            3.309585764294047,
            places=13,
        )
        self.assertAlmostEqual(
            self.fxs["expressive"].slope,
            0.3953928432516530,
            places=13,
        )
        self.assertAlmostEqual(
            self.fxs["expressive"].intercept,
            3.231954492415399,
            places=13,
        )

    def test_absolute_gap_derivatives(self):
        ds_m, ds_b = gap_coefficients(
            self.ds["receptive"], self.ds["expressive"]
        )
        fxs_m, fxs_b = gap_coefficients(
            self.fxs["receptive"], self.fxs["expressive"]
        )

        self.assertAlmostEqual(ds_m, 0.15131, places=12)
        self.assertAlmostEqual(ds_b, -2.728, places=12)
        self.assertAlmostEqual(fxs_m, 0.0543796188253598, places=13)
        self.assertAlmostEqual(fxs_b, 0.0776312718786481, places=13)

        ds_zero = -ds_b / ds_m
        self.assertAlmostEqual(ds_zero, 18.0292115524, places=9)

    def test_proportional_gap_derivative_numerators(self):
        ds_num = proportional_gap_derivative_numerator(
            self.ds["receptive"], self.ds["expressive"]
        )
        fxs_num = proportional_gap_derivative_numerator(
            self.fxs["receptive"], self.fxs["expressive"]
        )

        self.assertAlmostEqual(ds_num, 1.66174216, places=10)
        self.assertAlmostEqual(fxs_num, 0.145057604045, places=10)
        self.assertGreater(ds_num, 0)
        self.assertGreater(fxs_num, 0)

    def test_ae24_worked_example(self):
        A = 24.0

        expected = {
            "ds": {
                "t_r": 44.6801105538,
                "t_e": 56.6411579759,
                "g": 4.0325475279,
                "q": 1.2019560349,
                "h": 11.9610474221,
            },
            "fxs": {
                "t_r": 46.0019587241,
                "t_e": 52.5250921003,
                "g": 2.5792002525,
                "q": 1.1204063472,
                "h": 6.5231333762,
            },
        }

        for key, models in (("ds", self.ds), ("fxs", self.fxs)):
            r = models["receptive"]
            e = models["expressive"]
            t_r = r.inverse(A)
            t_e = e.inverse(A)
            g = float(score_gap(t_r, r, e))
            q = float(proportional_gap(t_r, r, e))
            h = float(time_gap(A, r, e))

            self.assertAlmostEqual(t_r, expected[key]["t_r"], places=9)
            self.assertAlmostEqual(t_e, expected[key]["t_e"], places=9)
            self.assertAlmostEqual(g, expected[key]["g"], places=9)
            self.assertAlmostEqual(q, expected[key]["q"], places=9)
            self.assertAlmostEqual(h, expected[key]["h"], places=9)

    def test_linear_mean_value_theorem_identity(self):
        """For the linear models, H(A) = G(t_R(A)) / m_E."""
        for models in (self.ds, self.fxs):
            r = models["receptive"]
            e = models["expressive"]
            for A in (12.0, 18.0, 24.0):
                t_r = r.inverse(A)
                lhs = time_gap(A, r, e)
                rhs = float(score_gap(t_r, r, e)) / e.slope
                self.assertAlmostEqual(lhs, rhs, places=12)

    def test_crossover_ages(self):
        ds_m, ds_b = gap_coefficients(
            self.ds["receptive"], self.ds["expressive"]
        )
        fxs_m, fxs_b = gap_coefficients(
            self.fxs["receptive"], self.fxs["expressive"]
        )

        absolute = (fxs_b - ds_b) / (ds_m - fxs_m)

        time_based = (
            (fxs_b / self.fxs["expressive"].slope)
            - (ds_b / self.ds["expressive"].slope)
        ) / (
            (ds_m / self.ds["expressive"].slope)
            - (fxs_m / self.fxs["expressive"].slope)
        )

        self.assertAlmostEqual(absolute, 28.94480799, places=7)
        self.assertAlmostEqual(time_based, 26.62605884, places=7)


if __name__ == "__main__":
    unittest.main()
