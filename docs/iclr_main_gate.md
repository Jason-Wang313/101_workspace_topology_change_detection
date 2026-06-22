# ICLR Main Gate

Paper: 101 workspace_topology_change_detection

Previous v3 decision: KILL_ARCHIVE

Current v5 gate verdict: STRONG_REVISE

ICLR-main readiness: no

## Gate Evidence

- Local benchmark: 6 tasks, 8 topology-change regimes, 8 splits, 15 methods.
- Seeds: 10.
- Episodes: 6 per method/task/regime/split/seed cell.
- Main rollouts: 345,600.
- Strongest non-oracle reference by success: `proposed_topology_change_detector_v4`.
- Proposed v5 versus strongest non-oracle success margin: `+0.12873`.
- Proposed v5 versus topological SLAM/TAMP success margin: `+0.24905`.
- Proposed v5 versus oracle success margin: `-0.10391`.
- Proposed v5 invalid-plan rate: `0.14149`.
- Proposed v5 collision/trap rate: `0.03385`.
- Proposed v5 support-failure rate: `0.01424`.
- Proposed v5 topology F1: `0.74339`.
- Proposed v5 ECE: `0.18972`.
- Proposed v5 utility: `0.43639`.
- Full method versus best removed-component ablation success margin: `+0.06154`.
- Fixed-risk strict v5: coverage `1.00000`, success `0.79427`, collision/trap `0.03351`, support failure `0.01215`.

## Passed Local Gates

- Success gate: passed.
- Invalid-plan gate: passed.
- Collision gate: passed.
- Support-failure gate: passed.
- Diagnostic gate: passed.
- Latency gate: passed.
- Regret gate: passed.
- Utility gate: passed.
- Calibration gate: passed.
- Ablation gate: passed.
- Stress gate: passed.
- Fixed-risk gate: passed.

## Failed Submission-Ready Gates

- No real robot validation.
- No accepted high-fidelity simulator benchmark validation.
- No accepted external benchmark validation.
- No calibrated external topology-change logs.
- No trained checkpoint or deployable model card.
- No rollout videos.
- Related-work synthesis is still not enough for a main-conference submission.

Conclusion: viable STRONG_REVISE project, not ICLR-main ready.
