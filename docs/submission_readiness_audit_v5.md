# Submission Readiness Audit v5

Paper: 101 workspace_topology_change_detection

Terminal decision: STRONG_REVISE

ICLR-main readiness: no

Canonical PDF: `C:/Users/wangz/Downloads/101.pdf`

PDF SHA256: `23709308E051A0E8AE6707EB14136BFB03AE954816511854137ABDBBF7ECBB92`

Page count: 25

## Frozen Protocol

- 6 tasks.
- 8 topology-change regimes.
- 8 splits.
- 15 methods.
- 10 seeds.
- 6 episodes per method/task/regime/split/seed cell.

## Produced Evidence

- Dataset summary rows: 3,840.
- Main rollout rows: 345,600.
- Main group rows: 57,600.
- Main seed rows: 150.
- Main metric rows: 120.
- Hard aggregate seed rows: 150.
- Hard aggregate metric rows: 15.
- Pairwise comparison rows: 14.
- Ablation rollout rows: 115,200.
- Stress rollout rows: 288,000.
- Fixed-risk rollout rows: 276,480.
- Negative cases: 24.

## Main Result

- v5 success: `0.80095 +/- 0.00707`.
- v5 invalid-plan: `0.14149`.
- v5 collision/trap: `0.03385`.
- v5 support failure: `0.01424`.
- v5 topology F1: `0.74339`.
- v5 ECE: `0.18972`.
- v5 regret: `0.10391`.
- v5 utility: `0.43639`.
- strongest non-oracle success: `0.67222 +/- 0.00988`.
- topological SLAM/TAMP success: `0.55191 +/- 0.01402`.
- oracle success: `0.90486 +/- 0.00460`.

## Gate Result

Passed local gates: success, invalid-plan, collision, support, diagnostic, latency, regret, utility, calibration, ablation, stress, fixed-risk.

Failed gate: scope.

## Required Before Submission

- Real robot validation or accepted high-fidelity benchmark validation.
- External benchmark comparison.
- Calibrated topology-change logs.
- Trained checkpoint and model card.
- Rollout videos and per-episode traces.
- Full manual related-work synthesis.
