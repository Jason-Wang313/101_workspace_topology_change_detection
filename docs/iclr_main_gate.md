# ICLR Main Gate

Paper: 101 workspace_topology_change_detection

Previous v3 decision: KILL_ARCHIVE

Current v4 gate verdict: STRONG_REVISE

## Gate Evidence

- Local benchmark: 5 tasks, 7 topology-change families, 5 splits, 9 methods.
- Seeds: 7.
- Episodes: 84 per method/task/family/split/seed group.
- Strongest non-oracle baseline: `topological_slam_tamp`.
- Proposed vs strongest baseline combined-stress success margin: `+0.114`.
- Proposed vs strongest invalid-plan delta: `-0.072`.
- Proposed vs strongest collision/trap delta: `-0.046`.
- Proposed vs strongest topology-F1 delta: `+0.142`.
- Proposed vs strongest detection-latency delta: `-0.120`.
- Full method vs best removed-component ablation margin: `+0.058`.

## Passed Local Gates

- Success gate: passed.
- Safety gate: passed.
- Diagnostic gate: passed.
- Pairwise seed gate: passed.
- Ablation gate: passed.

## Failed Submission-Ready Gates

- No real robot validation.
- No accepted external benchmark validation.
- No calibrated real topology-change logs.
- No trained checkpoint or full model card.
- No rollout videos.

Conclusion: viable STRONG_REVISE project, not ICLR-main ready.
