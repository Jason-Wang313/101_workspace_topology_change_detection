# Submission Readiness Audit v4.1

Paper: 101 `workspace_topology_change_detection`

Audit date: 2026-06-15

Decision: STRONG_REVISE

ICLR main readiness: no

## Fresh Rerun

Command sequence:

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python -m py_compile src\run_experiment.py
python src\run_experiment.py *> C:\Users\wangz\robotics_massive_pool_paper_factory\logs\101_workspace_topology_change_detection_continuation_rerun_20260615.log
```

The rerun completed successfully and printed `terminal_decision=STRONG_REVISE`.

## Coverage

- `metrics.csv`: 45 rows.
- `per_task_family_metrics.csv`: 1,575 rows.
- `seed_task_family_metrics.csv`: 11,025 rows.
- `seed_split_metrics.csv`: 315 rows.
- `pairwise_stats.csv`: 8 rows.
- `ablation_metrics.csv`: 7 rows.
- `ablation_seed_metrics.csv`: 49 rows.
- `ablation_task_family_seed_metrics.csv`: 1,715 rows.
- `stress_sweep.csv`: 54 rows.
- `stress_sweep_seed_metrics.csv`: 378 rows.
- `failure_cases.csv`: 8 rows.
- Seeds: 0 through 6.
- Tasks: `drawer_occluder_access`, `mobile_manipulation_movable_obstacles`, `narrow_passage_bin_pick`, `shelf_retrieval`, `support_dependency_rearrangement`.
- Topology-change families: `kinematic_trap_creation`, `object_stack_dependency_flip`, `occlusion_reveal_hide`, `passage_closure_opening`, `reachable_component_split_merge`, `support_removal`, `tool_access_tunnel_blockage`.

## Reproduced Local Evidence

- `proposed_topology_change_detector`: success 0.677 +/- 0.006, invalid plan 0.310, collision/trap 0.188, support failure 0.093, topology F1 0.635, latency 0.565, regret 0.152.
- `topological_slam_tamp`: success 0.564 +/- 0.005, invalid plan 0.382, collision/trap 0.234, support failure 0.130, topology F1 0.493, latency 0.685, regret 0.266.
- Paired proposed-vs-strongest success gain: 0.114 +/- 0.006, wins 7/7 seeds.
- Best removed-component ablation: `minus_replan_hysteresis`, success 0.622 vs full 0.680.
- Maximum topology stress: proposed success 0.678 vs `topological_slam_tamp` 0.549.

## Gate Outcome

The paper remains a strong local mechanism audit and should stay `STRONG_REVISE`. It is still not ICLR-main ready because it lacks real robot validation, accepted external benchmark validation, calibrated topology-change logs, trained model checkpoints, rollout videos, and a complete manual related-work synthesis.
