"""Generate Figure 1 from the shared developmental models."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from models import load_ds_models, load_fxs_models


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = REPO_ROOT / "figures" / "figure1_clean_trajectories.png"


def main() -> None:
    ds = load_ds_models()
    fxs = load_fxs_models()

    age = np.linspace(8, 63, 400)
    typical = age

    r_ds = ds["receptive"].value(age)
    e_ds = ds["expressive"].value(age)
    r_fxs = fxs["receptive"].value(age)
    e_fxs = fxs["expressive"].value(age)

    fig, ax = plt.subplots(figsize=(8.8, 5.4), dpi=200)

    ax.plot(
        age,
        typical,
        color="tab:blue",
        linestyle=":",
        linewidth=2.2,
        label="Typical reference: AE = age",
    )
    ax.plot(
        age,
        r_ds,
        color="tab:orange",
        linestyle="-",
        linewidth=2.2,
        label="DS receptive",
    )
    ax.plot(
        age,
        e_ds,
        color="tab:green",
        linestyle="--",
        linewidth=2.2,
        label="DS expressive",
    )
    ax.plot(
        age,
        r_fxs,
        color="tab:red",
        linestyle="-.",
        linewidth=2.2,
        label="FXS receptive",
    )
    ax.plot(
        age,
        e_fxs,
        color="tab:purple",
        linestyle=(0, (5, 2, 1, 2)),
        linewidth=2.2,
        label="FXS expressive",
    )

    ax.set_xlim(8, 63)
    ax.set_ylim(0, 64)
    ax.set_xlabel("Chronological age (months)")
    ax.set_ylabel("MSEL age-equivalent score (months)")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="upper left", ncol=2, frameon=True)

    fig.tight_layout()
    fig.savefig(OUTPUT, dpi=300, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
