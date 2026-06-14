# Submission Attack Log

Paper: 101 workspace_topology_change_detection

## Attack 1: No real robot validation

Verdict: still valid. This blocks ICLR-main readiness.

Action: mark STRONG_REVISE, not ready.

## Attack 2: No external benchmark

Verdict: still valid. Local evidence is not enough.

Action: require external manipulation/navigation validation before submission.

## Attack 3: Baselines are weak

Verdict: partly addressed. v4 adds topological SLAM/TAMP, graph-neural change classifier, robust replanning, uncertainty-triggered replanning, learned affordance maps, occupancy deltas, static scene graphs, and oracle.

Action: keep as STRONG_REVISE because the baselines are stronger but still proxy systems.

## Attack 4: The method only improves diagnostics

Verdict: addressed locally. It improves closed-loop success, invalid-plan rate, collision/trap rate, and support-failure rate.

Action: include closed-loop metrics in manuscript.

## Attack 5: Replanning cost might be hidden

Verdict: partially addressed. Replan cost is measured in the local benchmark, but not wall-clock robot time.

Action: report cost and list real-time validation as missing.

## Attack 6: Ablations may not isolate topology

Verdict: addressed locally. Removing support edges, passage homology, occlusion gates, action-conditioned prediction, or replan hysteresis reduces success.

Action: preserve ablation table.

## Attack 7: Related work is incomplete

Verdict: valid.

Action: require manual survey before submission.

## Terminal Action

STRONG_REVISE. Continue only with external experiments; do not submit this version to ICLR main.
