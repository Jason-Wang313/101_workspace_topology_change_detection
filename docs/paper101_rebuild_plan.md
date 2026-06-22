# Paper 101 Rebuild Plan: Workspace Topology Change Detection

Started: 2026-06-14 23:05:00 +0100

## Goal

Rebuild Paper 101 from a template archive into an honest ICLR-main-target evidence package if, and only if, the evidence supports it. The falsifiable claim is that detecting workspace topology changes before planning failure improves robot task success and safety under supports, passages, occlusions, and reachability changes.

## Claimed Mechanism

The proposed method, `proposed_topology_change_detector`, maintains an action-conditioned topology graph over:

- support relations;
- passability/reachability corridors;
- occlusion gates;
- stack dependencies;
- contact bridges;
- tool-access tunnels;
- kinematic dead-ends.

It should detect when the graph has changed enough that an old plan is invalid, and it should trigger targeted replanning before collision, trapping, support loss, or wasted execution.

## Benchmark To Build

Create a RAM-light executable benchmark with aggregate metrics rather than stored trajectories. The benchmark will cover:

- 5 tasks: shelf retrieval, bin picking through a narrow passage, drawer-with-occluder access, tabletop rearrangement with support dependencies, and mobile manipulation around movable obstacles.
- 7 topology-change families: passage closure/opening, support removal, occlusion reveal/hide, object-stack dependency flip, reachable-component split/merge, tool-access tunnel blockage, and kinematic trap creation.
- 5 splits: nominal, perception-noise shift, delayed-change shift, embodiment/reach shift, and combined stress.
- 9 methods: static scene-graph planner, occupancy-delta detector, learned affordance-map planner, uncertainty-triggered replanner, topological SLAM/TAMP baseline, graph-neural scene-change classifier, risk-aware robust replanner, proposed topology-change detector, and oracle topology planner.
- 7 random seeds with independent task/family episodes.

## Evidence Requirements

The rebuild must produce:

- Combined-stress task success, collision/trap/support-failure rate, invalid-plan rate, topology-change F1, detection latency, replan cost, and regret.
- Per-task/per-family breakdowns.
- Pairwise seed-level tests against the strongest non-oracle baseline.
- Stress sweep over topology-change intensity.
- Ablations for support-edge tracking, passage homology features, occlusion gates, action-conditioned prediction, and replan trigger thresholds.
- Failure cases explaining where topology detection is late, noisy, or unnecessary.
- Figures and LaTeX tables generated from CSVs.

## Terminal Gate

Mark `STRONG_REVISE` only if the proposed method:

- Beats the strongest non-oracle closed-loop baseline on combined-stress task success by a meaningful margin.
- Reduces invalid plans or collision/trap/support failures rather than merely replanning more often.
- Has better topology-change detection F1 or lower detection latency than non-topological replanning baselines.
- Wins paired seed comparisons against the strongest baseline.
- Survives core ablations: removing support edges, passage topology, occlusion gates, or action-conditioned prediction must not match the full method.
- States clearly that real robot/external benchmark validation is still missing.

Otherwise mark `KILL_ARCHIVE` with evidence.

## Execution Steps

1. Replace the shared probability script with a paper-specific topology-change benchmark.
2. Generate metrics, seed metrics, per-task/per-family tables, pairwise tests, stress sweep, ablations, failure cases, figures, and LaTeX tables.
3. Update repository docs to reflect the actual terminal gate.
4. Rewrite `paper/main.tex` as either a strong-revise evidence report or a negative archive report.
5. Compile and copy only `101.pdf` to `C:/Users/wangz/Downloads/101.pdf`.
6. Verify finite CSVs, py_compile, LaTeX log, PDF hash, no Desktop PDF, clean child repo, public GitHub push, and root report consistency.

## RAM Discipline

Use vectorized or aggregate group simulation and write summary tables directly. Keep all seeds, tasks, families, methods, stress levels, ablations, and failure cases; do not reduce experimental coverage to save memory.

## Execution Result

Completed: 2026-06-14 23:06:04 +0100

The benchmark was implemented and run. Terminal gate result: STRONG_REVISE. The proposed method beat `topological_slam_tamp` on combined-stress success, invalid-plan rate, collision/trap rate, topology F1, and detection latency, and no core ablation matched the full method. The paper remains not ICLR-main ready because external robot or accepted benchmark validation is missing.

## Continuation Result

Re-executed on 2026-06-15 under the Paper 101 ICLR-main submission-readiness plan. The historical v4.1 result remained `STRONG_REVISE`: the then-current topology-change detector beat topological SLAM/TAMP on combined-stress success, improved invalid-plan/collision/support safety, improved topology F1 and detection latency, won the paired seed gate, and no removed-component ablation matched the full method. It still was not ICLR-main ready without external robot or accepted benchmark validation.

## v5 Expanded Submission Result

Executed on 2026-06-22 under `docs/paper101_expanded_submission_plan_20260622.md`.

The benchmark was expanded to 6 tasks x 8 topology-change regimes x 8 splits x 15 methods x 10 seeds x 6 episodes per cell. The run produced 345,600 main rollouts, 115,200 ablation rollouts, 288,000 stress rollouts, 276,480 fixed-risk rollouts, and 24 negative cases.

Terminal result remained `STRONG_REVISE`. The new `risk_calibrated_topology_belief_v5` reached hard-aggregate success `0.80095`, beating the strongest non-oracle v4 reference at `0.67222` and topological SLAM/TAMP at `0.55191`, while reducing invalid plans, collision/trap failures, support failures, ECE, regret, and improving utility. All local empirical gates passed. The scope gate failed because there is still no real robot, accepted high-fidelity benchmark, external benchmark, calibrated topology-change log, trained checkpoint, or rollout-video evidence.
