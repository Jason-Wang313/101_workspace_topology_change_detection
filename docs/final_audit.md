# Final Audit

Paper 101 v5 was rebuilt and rerun as a hostile-review workspace-topology evidence audit.

## Evidence Audit

The benchmark evaluates risk-calibrated action-conditioned topology belief across 6 tasks, 8 topology-change regimes, 8 splits, 15 methods, 10 seeds, and 6 episodes per method/task/regime/split/seed cell. The run produced 345,600 main rollouts, 115,200 ablation rollouts, 288,000 stress rollouts, 276,480 fixed-risk rollouts, and 24 negative cases.

The proposed `risk_calibrated_topology_belief_v5` beats every non-oracle baseline on hard-aggregate success and utility while reducing invalid plans, collision/trap failures, support failures, regret, and calibration error relative to the strongest non-oracle reference.

## Terminal Decision

STRONG_REVISE.

The mechanism is strong enough to keep as an ICLR-main-target research project. It is not submission-ready and must not be framed as validated robotics deployment.

## Verification Targets

- Re-run: `python src\run_experiment.py`.
- Manuscript generator: `python scripts\generate_manuscript.py`.
- Submission validator: `python scripts\validate_submission_artifacts.py`.
- Main evidence: `results/metrics.csv`, `results/hard_aggregate_metrics.csv`, `results/main_seed_metrics.csv`, `results/pairwise_stats.csv`.
- Ablation evidence: `results/ablation_metrics.csv`, `results/ablation_seed_metrics.csv`.
- Stress evidence: `results/stress_sweep.csv`, `results/stress_sweep_seed_metrics.csv`.
- Fixed-risk evidence: `results/fixed_risk_metrics.csv`, `results/fixed_risk_pairwise_stats.csv`.
- PDF target: `C:/Users/wangz/Downloads/101.pdf`.
- PDF SHA256: `23709308E051A0E8AE6707EB14136BFB03AE954816511854137ABDBBF7ECBB92`.
