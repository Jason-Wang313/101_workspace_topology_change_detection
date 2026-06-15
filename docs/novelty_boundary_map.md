# Novelty Boundary Map

## Crowded Territory

- Static scene graphs.
- Occupancy-grid change detection.
- Dynamic scene graphs.
- Topological SLAM.
- Generic uncertainty-triggered replanning.
- Robust TAMP without explicit topology-change diagnosis.
- Learned affordance maps without action-conditioned graph updates.

## Claimed Boundary

The local contribution is action-conditioned workspace topology-change detection: support edges, passage connectivity, occlusion gates, stack dependencies, tool tunnels, and kinematic traps are tracked as planning-relevant graph changes.

## Current Evidence

The proposed method locally beats topological SLAM/TAMP, graph-neural change classification, robust replanning, and occupancy-delta baselines under combined stress while reducing invalid plans and collision/trap failures. The 2026-06-15 continuation rerun reproduced this pattern.

## Boundary Still Not Proven Externally

The claim is not yet proven on robot hardware, accepted benchmarks, or real dynamic-scene logs.
