# Reproducibility Checklist

- Code entry point: `src/run_experiment.py`.
- Dependencies: `numpy`, `matplotlib`.
- Deterministic base seed: `101_2026`.
- Seeds: `0..6`.
- Results directory: `results/`.
- Figures directory: `figures/`.
- Tables are generated from CSV outputs.
- 2026-06-15 continuation log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/101_workspace_topology_change_detection_continuation_rerun_20260615.log`.
- PDF can be rebuilt with `pdflatex`, `bibtex`, and two final `pdflatex` passes in `paper/`.

## Known Limits

- The benchmark is local rather than hardware-calibrated.
- Full trajectories are not stored to keep RAM and disk use light.
- No external benchmark data is consumed.
- No trained model checkpoint is released.
