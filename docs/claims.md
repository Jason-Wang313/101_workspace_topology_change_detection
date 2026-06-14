# Claims

## Supported Local Claim

Action-conditioned topology-change detection improves planning under changing supports, passages, occlusions, reachability components, tool-access tunnels, and kinematic traps.

## Evidence

- Proposed combined-stress success: `0.677 +/- 0.006`.
- Strongest non-oracle baseline, `topological_slam_tamp`: `0.564 +/- 0.005`.
- Proposed invalid-plan, collision/trap, and support-failure rates are lower than the strongest baseline.
- Proposed topology F1 is higher and detection latency is lower than the strongest baseline.
- Pairwise proposed-vs-strongest success difference: `0.114 +/- 0.006`, winning `7/7` seeds.
- Ablations removing support edges, passage homology, occlusion gates, action-conditioned prediction, or replan hysteresis reduce success or worsen risk.

## Scope

The claim is local. It does not prove real robot performance, external benchmark superiority, or general scene-graph planning dominance.
