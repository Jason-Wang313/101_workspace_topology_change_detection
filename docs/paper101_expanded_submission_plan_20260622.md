# Paper 101 Expanded Submission Plan

Date: 2026-06-22

Paper: `101_workspace_topology_change_detection`

Target: rebuild Paper 101 into a 25+ page ICLR-style evidence package if, and only if, the expanded local evidence survives hostile review.

Terminal policy: do not optimize for pretty results. Optimize for a result that survives hostile review.

Use strong baselines and stress tests to expose weaknesses, improve the method during development, then freeze the final protocol and report all predefined results honestly.

## Starting Point

The v4.1 continuation audit is locally positive but not submission-ready:

- The proposed action-conditioned topology-change detector beats `topological_slam_tamp` on combined-stress success, `0.677` vs `0.564`.
- It reduces invalid plans, collision/trap failures, support failures, topology detection latency, and oracle regret.
- It remains blocked by no real robot evidence, no accepted external benchmark, no calibrated topology-change logs, no trained checkpoint, no videos, and incomplete manual related-work synthesis.

The v5 pass must strengthen local evidence without pretending that local evidence is external validation.

## Claim Under Test

Action-conditioned, risk-calibrated topology belief should improve closed-loop manipulation/navigation when the workspace graph changes through supports, passages, occlusions, reachable components, tool corridors, kinematic traps, and dynamic affordance inversions.

The claim is not "topology always wins." The claim is narrower:

> preserving calibrated topology-change belief, action-conditioned graph deltas, support/passage memory, active probes, hysteresis, and fixed-risk filtering should improve hard local outcomes over topological SLAM/TAMP, robust replanning, particle-filter topology belief, conformal filtering, graph classifiers, and scene-graph planning proxies.

## Expanded CPU-Only Protocol

Keep the experiment CPU-only and RAM-light by streaming rollout rows to CSV and aggregating online. Do not reduce evidence quality to save RAM.

Main design:

- Tasks: 6.
- Topology-change regimes: 8.
- Splits: 8.
- Methods: 15.
- Seeds: 10.
- Episodes per seed/task/regime/split/method cell: 6.
- Expected main rollout rows: 345,600.

### Tasks

1. `shelf_retrieval`
2. `narrow_passage_bin_pick`
3. `drawer_occluder_access`
4. `support_dependency_rearrangement`
5. `mobile_manipulation_movable_obstacles`
6. `tool_corridor_reconfiguration`

### Topology-Change Regimes

1. `passage_closure_opening`
2. `support_removal`
3. `occlusion_reveal_hide`
4. `object_stack_dependency_flip`
5. `reachable_component_split_merge`
6. `tool_access_tunnel_blockage`
7. `kinematic_trap_creation`
8. `dynamic_affordance_inversion`

### Splits

1. `nominal`
2. `perception_noise_shift`
3. `delayed_change_shift`
4. `embodiment_reach_shift`
5. `support_cascade_shift`
6. `false_topology_alarm_shift`
7. `latency_budget_shift`
8. `combined_extreme`

### Methods

1. `static_scene_graph_planner`
2. `occupancy_delta_replanner`
3. `learned_affordance_map`
4. `uncertainty_triggered_replanner`
5. `topological_slam_tamp`
6. `graph_neural_change_classifier`
7. `risk_aware_robust_replanner`
8. `conformal_topology_risk_filter`
9. `particle_filter_topology_belief_mpc`
10. `dynamic_scene_graph_transformer_proxy`
11. `neural_tamp_replanner`
12. `active_view_topology_probe`
13. `proposed_topology_change_detector_v4`
14. `risk_calibrated_topology_belief_v5`
15. `oracle_topology_planner`

## Metrics

Main metrics:

- Task success.
- Invalid-plan rate.
- Collision/trap rate.
- Support-failure rate.
- Topology F1.
- Missed-change false-negative rate.
- False-topology-alarm rate.
- Detection latency.
- Replan cost.
- Expected calibration error for topology risk.
- Regret to oracle.
- Robust utility.

Derived evidence:

- Main per-cell rollout CSV.
- Per task/regime/split/method aggregate CSV.
- Seed-level metrics.
- Hard-regime aggregate metrics.
- Pairwise seed tests against every non-v5 method.
- Ablation tables.
- Stress-sweep tables.
- Fixed-risk deployment tables.
- Negative-case ledger.

## Ablations

1. `full_risk_calibrated_topology_belief_v5`
2. `no_action_conditioning`
3. `no_support_edge_memory`
4. `no_passage_homology`
5. `no_occlusion_persistence`
6. `no_replan_hysteresis`
7. `no_topology_risk_calibration`
8. `no_active_topology_probe`
9. `v4_topology_detector_rules`
10. `topological_slam_only`

## Stress Tests

Run a ten-level stress sweep over topology-change severity, perception ambiguity, delayed observation, reachability shift, support cascade, false topology alarms, and latency budget pressure.

Hardest stress point must compare v5 against:

- `topological_slam_tamp`
- `particle_filter_topology_belief_mpc`
- `conformal_topology_risk_filter`
- `risk_aware_robust_replanner`
- `active_view_topology_probe`
- `oracle_topology_planner`

## Fixed-Risk Deployment

Evaluate deployment under strict collision/trap and support-failure budgets.

Budgets:

- `strict`: collision/trap <= 0.05 and support failure <= 0.04.
- `moderate`: collision/trap <= 0.08 and support failure <= 0.06.

Report coverage, success, invalid-plan rate, collision/trap rate, support-failure rate, and utility. Fixed-risk success must not be fabricated by simply abstaining on almost everything.

## Local Empirical Gates

The paper can remain STRONG_REVISE only if all local empirical gates pass:

1. Success gate: v5 hard success exceeds the best non-oracle success reference by at least `0.05`.
2. Invalid-plan gate: v5 invalid-plan rate is below the best non-oracle safety reference, or within `0.015` while improving success and utility materially.
3. Collision/support gate: v5 collision/trap and support-failure rates are both below the best non-oracle safety reference, or within `0.015` with better fixed-risk coverage.
4. Diagnostic gate: v5 topology F1 exceeds the best non-oracle diagnostic reference or ties while improving missed-change false negatives.
5. Latency gate: v5 latency is below the strongest closed-loop baseline, or lower latency is traded for materially better safety and success.
6. Regret gate: v5 regret to oracle is below the best non-oracle regret reference.
7. Utility gate: v5 robust utility exceeds the best non-oracle utility reference.
8. Calibration gate: v5 topology-risk ECE is no worse than conformal filtering plus `0.01`, while improving success.
9. Ablation gate: no removed-component ablation may match or beat the full method on both success and safety.
10. Stress gate: at maximum stress, v5 remains above the strongest non-oracle reference on robust utility.
11. Fixed-risk gate: v5 satisfies strict budgets with useful coverage above `0.20`.

## Scope Gate

ICLR-main readiness remains `no` unless all of these exist:

- Real robot validation or accepted high-fidelity benchmark validation.
- External benchmark comparison.
- Calibrated topology-change event logs or equivalent external data.
- Trained checkpoint or deployable model artifact.
- Rollout/video evidence.
- Manual related-work synthesis.

This v5 CPU-only pass is expected to fail the scope gate. If local empirical gates pass and only the scope gate fails, terminal state is `STRONG_REVISE`, not submission-ready.

## Kill Rule

If any local empirical gate fails, mark the paper `KILL_ARCHIVE` and report the strongest failure. Do not bury a failure under a polished 25+ page PDF.

## Manuscript Requirements

- At least 25 pages without filler.
- Add theory: topology-belief state, action-conditioned graph-update operator, calibration/fixed-risk lemma, and an impossibility/identifiability limitation.
- Add experiments: expanded baselines, stress, ablations, fixed-risk deployment, negative cases, and hard-regime aggregate tables.
- Use bright boxed clickable citations in the PDF.
- Put the numbered PDF only at `C:/Users/wangz/Downloads/101.pdf`.
- Do not copy the PDF to the visible Desktop.

## Execution Steps

1. Replace the v4.1 runner with a streaming v5 runner.
2. Run `python src\run_experiment.py`.
3. If the frozen local gates fail, keep the failure and write a KILL_ARCHIVE manuscript.
4. If gates pass, build the STRONG_REVISE manuscript honestly, still with scope-gate failure.
5. Generate `paper/main.tex`, `paper/references.bib`, figures, tables, and validation scripts.
6. Compile the PDF with `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`.
7. Copy only `paper/main.pdf` to `C:/Users/wangz/Downloads/101.pdf`.
8. Validate row counts, PDF page count, hash, boxed citation settings, no repo-local `101.pdf`, no Desktop copy, Python syntax, LaTeX references, and GitHub state.
9. Push the public GitHub repo.
10. Update root ledgers and move the frontier to Paper 102.
