# Paper

`one-gap-three-answers.pdf` is the final paper associated with this repository:

**Nicole Rollo. "One Gap, Three Answers: A Calculus Analysis of Receptive and Expressive Language Development." MATH 140: Calculus I, University of Maryland Global Campus, 2026.**

The PDF is a format conversion of the authoritative final DOCX used to build this public repository. The mathematical content, conclusions, figures, and original appendices have not been rewritten for GitHub.

The paper's appendices contain the original figure-generation scripts. The code in `../src/` is a cleaned reproducibility refactor: common model construction is centralized, published FXS aggregate means are read from `../data/`, DS intercepts are reconstructed from their documented inputs, and both figures use the same shared models.

The refactor was verified against the final paper before documentation was added. It reproduces the reported numerical results, both crossover ages, and the final DOCX figure PNGs without changing the underlying mathematics.

For a concise technical overview and reproduction instructions, see the repository-level `README.md`.


## License

The original written content of the paper is © 2026 Nicole Rollo and is made available under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license, except for third-party material cited from external sources. See `../LICENSE-CONTENT.md`.
