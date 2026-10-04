# Data and model-input provenance

This directory contains only the small set of published aggregate values and documented modeling inputs required to reproduce the final Calculus I analysis.

It does **not** contain participant-level data, digitized pseudo-observations, complete copies of source-study tables or figures, or the source articles themselves.

## Provenance categories

The repository distinguishes three kinds of quantities:

1. **Published aggregate values** - values reported by the source studies.
2. **Project modeling choices** - quantities estimated or constructed by Nicole Rollo for the calculus analysis.
3. **Derived mathematical results** - regression coefficients, intercepts, gap measures, derivatives, and crossover ages calculated from the model inputs.

That distinction should be preserved in any reuse of this repository.

## `ds_model_inputs.csv`

The Down syndrome models in the final paper are

$$
R_{DS}(t)=0.48845t+2.176
$$

$$
E_{DS}(t)=0.33714t+4.904.
$$

D'Souza et al. (2026) did not report those slope/intercept pairs directly. The project constructed them in two steps.

### Step 1: estimate slopes from the published trajectories

The cross-sectional receptive- and expressive-language slopes were estimated by the project author from **Figure 2** of D'Souza et al. (2026):

| Trajectory | Estimated slope |
|---|---:|
| Receptive language | 0.48845 |
| Expressive language | 0.33714 |

These values are **author estimates from a published figure**, not regression coefficients reported by D'Souza et al.

### Step 2: anchor the slopes to published Table 2 means

D'Souza et al. Table 2 reports the following Time 1 cross-sectional means used by the project:

| Quantity | Published mean |
|---|---:|
| Chronological age | 27.81 months |
| Receptive-language AE | 15.76 months |
| Expressive-language AE | 14.28 months |

For a line $`y=mt+b`$, the intercept is

$$
b=y-mt.
$$

Therefore:

$$
b_R=15.76-(0.48845)(27.81)=2.1762055
$$

and

$$
b_E=14.28-(0.33714)(27.81)=4.9041366.
$$

The final paper and its original Python appendices use the three-decimal intercepts

$$
b_R=2.176, \qquad b_E=4.904.
$$

The repository reconstructs those values from `ds_model_inputs.csv` and then applies the same rounding so that the public code reproduces the authoritative final-paper equations exactly.

### Source

D'Souza, H., Karmiloff-Smith, A., Mareschal, D., & Thomas, M. S. C. (2026). *The Down syndrome profile emerges gradually across early development*. Journal of Applied Research in Intellectual Disabilities, 39(4), Article e70218. https://doi.org/10.1111/jar.70218

## `fxs_roberts2009_tableII.csv`

Roberts et al. (2009) reported MSEL age-cluster means for boys with Fragile X syndrome. The final project fit separate ordinary least-squares lines to the receptive- and expressive-language means using the nominal cluster ages as $`t`$-values.

The seven aggregate rows used are:

| Nominal cluster age (mo) | Receptive AE mean (mo) | Expressive AE mean (mo) |
|---:|---:|---:|
| 9 | 7.00 | 6.18 |
| 12 | 8.94 | 7.76 |
| 18 | 10.68 | 9.42 |
| 24 | 14.53 | 13.71 |
| 36 | 19.27 | 18.17 |
| 48 | 27.21 | 24.55 |
| 60 | 28.64 | 24.68 |

`src/models.py` reads these rows and recomputes the OLS fits with `numpy.polyfit`. The resulting unrounded coefficients are retained for calculations:

```text
FXS receptive:
  slope     = 0.4497724620770128
  intercept = 3.309585764294047

FXS expressive:
  slope     = 0.3953928432516530
  intercept = 3.231954492415399
```

The final paper displays rounded equations but performs its FXS calculations with the unrounded coefficients.

The published clusters represent **age ranges**, not exact single-age observations. Using the nominal cluster ages is therefore a project modeling choice. These fitted lines approximate the published group trend and are not reproductions of the hierarchical linear models reported by Roberts et al.

### Source

Roberts, J. E., Mankowski, J. B., Sideris, J., Goldman, B. D., Hatton, D. D., Mirrett, P. L., Baranek, G. T., Reznick, J. S., Long, A. C. J., & Bailey, D. B., Jr. (2009). *Trajectories and predictors of the development of very young boys with fragile X syndrome*. Journal of Pediatric Psychology, 34(8), 827-836. https://doi.org/10.1093/jpepsy/jsn129

## What is deliberately excluded

This directory does not include:

- participant-level data from either study;
- screenshots or copies of the source articles, tables, or figures;
- reconstructed individual observations;
- a "typical development" dataset - the `AE = chronological age` line is a normalized reference model, not empirical data;
- MSEL domains that were not inputs to the receptive-expressive calculus analysis;
- correlations, demographic tables, or other source-study statistics that were not used to construct the models.

The purpose of this directory is reproducibility of the published Calculus I project, not secondary analysis of the underlying studies.
