"""Generate Figure 2 from the shared developmental models."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

from models import load_ds_models, load_fxs_models, time_gap


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = REPO_ROOT / "figures" / "figure2_time_gap_example.png"


def main() -> None:
    ds = load_ds_models()
    fxs = load_fxs_models()

    r_ds = ds["receptive"]
    e_ds = ds["expressive"]
    r_fxs = fxs["receptive"]
    e_fxs = fxs["expressive"]

    A = 24.0

    t_r_ds = r_ds.inverse(A)
    t_e_ds = e_ds.inverse(A)
    t_r_fxs = r_fxs.inverse(A)
    t_e_fxs = e_fxs.inverse(A)

    h_ds = time_gap(A, r_ds, e_ds)
    h_fxs = time_gap(A, r_fxs, e_fxs)

    age = np.linspace(41, 58.5, 300)

    fig, ax = plt.subplots(figsize=(8.8, 4.8), dpi=200)

    ax.plot(
        age,
        r_ds.value(age),
        color="tab:orange",
        linestyle="-",
        linewidth=2.0,
        label="DS receptive",
    )
    ax.plot(
        age,
        e_ds.value(age),
        color="tab:green",
        linestyle="--",
        linewidth=2.0,
        label="DS expressive",
    )
    ax.plot(
        age,
        r_fxs.value(age),
        color="tab:red",
        linestyle="-.",
        linewidth=2.0,
        label="FXS receptive",
    )
    ax.plot(
        age,
        e_fxs.value(age),
        color="tab:purple",
        linestyle=(0, (5, 2, 1, 2)),
        linewidth=2.0,
        label="FXS expressive",
    )

    ax.axhline(A, color="gray", linewidth=1.2, alpha=0.75)
    ax.text(
        41.2,
        24.35,
        "AE = 24",
        color="gray",
        fontsize=10,
        bbox=dict(
            boxstyle="round,pad=0.2",
            facecolor="white",
            edgecolor="none",
            alpha=0.8,
        ),
    )

    points = [
        (t_r_ds, A),
        (t_e_ds, A),
        (t_r_fxs, A),
        (t_e_fxs, A),
    ]

    for t_value, ae_value in points:
        ax.vlines(
            t_value,
            ymin=20,
            ymax=ae_value,
            color="gray",
            linewidth=1.0,
            linestyles=":",
            alpha=0.6,
        )
        ax.plot(t_value, ae_value, "o", color="black", markersize=4)

    ax.add_patch(
        FancyArrowPatch(
            (t_r_ds, 24.9),
            (t_e_ds, 24.9),
            arrowstyle="<->",
            mutation_scale=10,
            linewidth=1.4,
        )
    )
    ax.text(
        (t_r_ds + t_e_ds) / 2,
        25.45,
        f"DS gap = {h_ds:.2f} mo",
        ha="center",
        va="bottom",
        fontsize=10,
        bbox=dict(
            boxstyle="round,pad=0.25",
            facecolor="white",
            edgecolor="gray",
            alpha=0.95,
        ),
    )

    ax.add_patch(
        FancyArrowPatch(
            (t_r_fxs, 22.9),
            (t_e_fxs, 22.9),
            arrowstyle="<->",
            mutation_scale=10,
            linewidth=1.4,
        )
    )
    ax.text(
        (t_r_fxs + t_e_fxs) / 2,
        22.35,
        f"FXS gap = {h_fxs:.2f} mo",
        ha="center",
        va="top",
        fontsize=10,
        bbox=dict(
            boxstyle="round,pad=0.25",
            facecolor="white",
            edgecolor="gray",
            alpha=0.95,
        ),
    )

    ax.text(t_r_ds, 20.25, f"{t_r_ds:.2f}", ha="center", va="bottom", fontsize=9)
    ax.text(t_r_fxs, 20.25, f"{t_r_fxs:.2f}", ha="center", va="bottom", fontsize=9)
    ax.text(t_e_fxs, 20.25, f"{t_e_fxs:.2f}", ha="center", va="bottom", fontsize=9)
    ax.text(t_e_ds, 20.25, f"{t_e_ds:.2f}", ha="center", va="bottom", fontsize=9)

    ax.set_xlim(41, 58.5)
    ax.set_ylim(20, 28)
    ax.set_xlabel("Chronological age (months)")
    ax.set_ylabel("MSEL age-equivalent score (months)")
    ax.grid(True, alpha=0.22)
    ax.legend(loc="upper left", ncol=2, frameon=True)

    fig.tight_layout()
    fig.savefig(OUTPUT, dpi=300, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
