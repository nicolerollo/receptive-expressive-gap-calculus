"""Reproduce the numerical calculus results reported in the final paper."""

from __future__ import annotations

from models import (
    gap_coefficients,
    load_ds_models,
    load_fxs_models,
    proportional_gap,
    proportional_gap_derivative_numerator,
    score_gap,
    time_gap,
)


def solve_linear_equality(
    slope_a: float,
    intercept_a: float,
    slope_b: float,
    intercept_b: float,
) -> float:
    """Solve slope_a*t + intercept_a = slope_b*t + intercept_b."""
    return (intercept_b - intercept_a) / (slope_a - slope_b)


def main() -> None:
    ds = load_ds_models()
    fxs = load_fxs_models()

    r_ds, e_ds = ds["receptive"], ds["expressive"]
    r_fxs, e_fxs = fxs["receptive"], fxs["expressive"]

    g_ds_m, g_ds_b = gap_coefficients(r_ds, e_ds)
    g_fxs_m, g_fxs_b = gap_coefficients(r_fxs, e_fxs)

    qprime_ds_num = proportional_gap_derivative_numerator(r_ds, e_ds)
    qprime_fxs_num = proportional_gap_derivative_numerator(r_fxs, e_fxs)

    ds_zero_crossing = -g_ds_b / g_ds_m

    A = 24.0

    def summarize(label, r, e):
        t_r = r.inverse(A)
        t_e = e.inverse(A)
        g = float(score_gap(t_r, r, e))
        q = float(proportional_gap(t_r, r, e))
        h = float(time_gap(A, r, e))
        return {
            "label": label,
            "t_R": t_r,
            "t_E": t_e,
            "G": g,
            "Q": q,
            "H": h,
        }

    ds24 = summarize("DS", r_ds, e_ds)
    fxs24 = summarize("FXS", r_fxs, e_fxs)

    absolute_crossover = solve_linear_equality(
        g_ds_m, g_ds_b, g_fxs_m, g_fxs_b
    )

    # At chronological age t, the time gap associated with the score R(t)
    # is G(t) / m_E for these linear models.
    time_crossover = solve_linear_equality(
        g_ds_m / e_ds.slope,
        g_ds_b / e_ds.slope,
        g_fxs_m / e_fxs.slope,
        g_fxs_b / e_fxs.slope,
    )

    print("MODEL COEFFICIENTS")
    print(f"DS receptive   : slope={r_ds.slope:.14f}, intercept={r_ds.intercept:.14f}")
    print(f"DS expressive  : slope={e_ds.slope:.14f}, intercept={e_ds.intercept:.14f}")
    print(f"FXS receptive  : slope={r_fxs.slope:.14f}, intercept={r_fxs.intercept:.14f}")
    print(f"FXS expressive : slope={e_fxs.slope:.14f}, intercept={e_fxs.intercept:.14f}")

    print("\nABSOLUTE GAP")
    print(f"G_DS(t)  = {g_ds_m:.14f} t + ({g_ds_b:.14f})")
    print(f"G_FXS(t) = {g_fxs_m:.14f} t + ({g_fxs_b:.14f})")
    print(f"G'_DS    = {g_ds_m:.14f}")
    print(f"G'_FXS   = {g_fxs_m:.14f}")
    print(f"DS sign change = {ds_zero_crossing:.8f} months")

    print("\nPROPORTIONAL GAP DERIVATIVE NUMERATORS")
    print(f"DS  : {qprime_ds_num:.12f}")
    print(f"FXS : {qprime_fxs_num:.12f}")

    print("\nAE = 24 WORKED EXAMPLE")
    for result in (ds24, fxs24):
        print(
            f"{result['label']}: "
            f"t_R={result['t_R']:.10f}, "
            f"t_E={result['t_E']:.10f}, "
            f"G={result['G']:.10f}, "
            f"Q={result['Q']:.10f}, "
            f"H={result['H']:.10f}"
        )

    print("\nPAPER-ROUNDED AE = 24 RESULTS")
    print(
        f"DS : t_R={ds24['t_R']:.2f}, t_E={ds24['t_E']:.2f}, "
        f"G={ds24['G']:.2f}, Q-1={(ds24['Q'] - 1) * 100:.1f}%, "
        f"H={ds24['H']:.2f}"
    )
    print(
        f"FXS: t_R={fxs24['t_R']:.2f}, t_E={fxs24['t_E']:.2f}, "
        f"G={fxs24['G']:.2f}, Q-1={(fxs24['Q'] - 1) * 100:.1f}%, "
        f"H={fxs24['H']:.2f}"
    )

    print("\nDS / FXS RATIOS AT AE = 24")
    print(f"absolute score gap : {ds24['G'] / fxs24['G']:.2f}")
    print(
        "proportional excess: "
        f"{(ds24['Q'] - 1) / (fxs24['Q'] - 1):.2f}"
    )
    print(f"chronological gap  : {ds24['H'] / fxs24['H']:.2f}")

    print("\nCROSSOVERS")
    print(f"absolute-gap equality: {absolute_crossover:.8f} months")
    print(f"time-gap equality    : {time_crossover:.8f} months")


if __name__ == "__main__":
    main()
