# Paper 101 Terminal Audit - 2026-06-15

Paper: `101_workspace_topology_change_detection`

Final decision: STRONG_REVISE

ICLR main ready: no

## What Was Rechecked

- A paper-specific ICLR-main readiness execution plan was written before rerunning experiments.
- `src/run_experiment.py` compiled successfully.
- The full benchmark reran successfully with seven seeds and saved a continuation log.
- CSV, table, figure, summary, and manuscript artifacts were regenerated.
- The terminal decision in `results/summary.txt` was re-audited against the predeclared gates.

## Why It Stays Alive

The local mechanism reproduced:

- Proposed combined-stress success is 0.677 vs 0.564 for `topological_slam_tamp`.
- Proposed invalid-plan rate is 0.310 vs 0.382 for the strongest baseline.
- Proposed collision/trap rate is 0.188 vs 0.234 for the strongest baseline.
- Proposed topology F1 is 0.635 vs 0.493 for the strongest baseline.
- Proposed detection latency is 0.565 vs 0.685 for the strongest baseline.
- Paired success gain against `topological_slam_tamp` is 0.114 +/- 0.006 with 7/7 seed wins.
- Core removed-component ablations remain below full.
- At maximum topology stress, proposed success is 0.678 vs 0.549 for `topological_slam_tamp`.

## Why It Is Still Not Submission Ready

- No real robot validation.
- No accepted external manipulation or navigation benchmark.
- No calibrated real topology-change logs.
- No trained topology-change model checkpoint or model card.
- No hardware or benchmark rollout videos.
- Related work still needs a full manual synthesis.

## Artifact Policy

- Canonical PDF: `C:/Users/wangz/Downloads/101.pdf`.
- Visible Desktop PDF copy: prohibited.
- GitHub repository: https://github.com/Jason-Wang313/101_workspace_topology_change_detection

## Terminal Action

Keep Paper 101 as `STRONG_REVISE`, not submission-ready. The next real work would be real robot or accepted external benchmark validation against dynamic scene-graph, topological SLAM/TAMP, robust replanning, and learned-affordance baselines.
