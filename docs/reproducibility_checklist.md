# Reproducibility Checklist

- Code entry point: `src/run_experiment.py`.
- Manuscript generator: `scripts/generate_manuscript.py`.
- Artifact validator: `scripts/validate_submission_artifacts.py`.
- Dependencies: `numpy`, `matplotlib`, LaTeX, BibTeX.
- Deterministic base seed: `101_2026`.
- Seeds: `0..9`.
- Results directory: `results/`.
- Figures directory: `figures/`.
- Tables are generated from CSV outputs.
- Canonical PDF path: `C:/Users/wangz/Downloads/101.pdf`.
- PDF SHA256: `23709308E051A0E8AE6707EB14136BFB03AE954816511854137ABDBBF7ECBB92`.
- PDF page count: 25.
- PDF can be rebuilt with `pdflatex`, `bibtex`, and two final `pdflatex` passes in `paper/`.

## Known Limits

- The benchmark is local rather than hardware-calibrated.
- Full trajectories are not stored to keep RAM and disk use light.
- No external benchmark data is consumed.
- No trained model checkpoint is released.
- Videos are not released.
