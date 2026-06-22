# Novelty Boundary Map

## Crowded Territory

- Static scene graphs.
- Occupancy-grid change detection.
- Dynamic scene graphs.
- Topological SLAM.
- Generic uncertainty-triggered replanning.
- Robust TAMP without explicit topology-change diagnosis.
- Learned affordance maps without action-conditioned graph updates.
- Conformal risk filtering without topology-specific belief state.
- Particle-filter belief MPC without explicit support/passage/occlusion topology.

## Claimed Boundary

The local contribution is risk-calibrated action-conditioned workspace topology belief: support edges, passage connectivity, occlusion gates, stack dependencies, reachable components, tool tunnels, and kinematic traps are tracked as planning-relevant graph changes with fixed-risk reporting.

## Current Evidence

The proposed v5 method locally beats topological SLAM/TAMP, graph-neural change classification, robust replanning, conformal risk filtering, particle-filter belief MPC, dynamic scene-graph transformer proxy, neural TAMP, active probing, occupancy-delta, learned-affordance, and v4 detector baselines under a frozen combined benchmark. It reduces invalid plans, collision/trap failures, support failures, ECE, regret, and improves utility.

## Boundary Still Not Proven Externally

The claim is not yet proven on robot hardware, accepted benchmarks, real dynamic-scene logs, or a trained deployable model.
