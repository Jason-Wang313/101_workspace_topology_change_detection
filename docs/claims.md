# Claims

## Supported Local Claim

Risk-calibrated action-conditioned topology belief improves closed-loop planning in a local CPU-only benchmark of changing workspace topology. The claim covers changing supports, passages, occlusions, stack dependencies, reachability splits/merges, tool tunnels, kinematic traps, and dynamic affordance inversions.

## Evidence

- Benchmark: 6 tasks x 8 topology-change regimes x 8 splits x 15 methods x 10 seeds x 6 episodes per cell.
- Main rollouts: 345,600.
- Proposed v5 hard-aggregate success: `0.80095 +/- 0.00707`.
- Strongest non-oracle reference, `proposed_topology_change_detector_v4`: `0.67222 +/- 0.00988`.
- Topological SLAM/TAMP baseline: `0.55191 +/- 0.01402`.
- Oracle reference: `0.90486 +/- 0.00460`.
- Safety: v5 invalid-plan `0.14149`, collision/trap `0.03385`, support failure `0.01424`, all below the strongest non-oracle reference.
- Diagnostics: v5 topology F1 `0.74339`, missed-change false negative rate `0.36731`, false-alarm rate `0.14104`, latency `0.61527`, ECE `0.18972`.
- Utility/regret: v5 utility `0.43639`, regret `0.10391`.
- Pairwise margins: v5 beats every non-oracle baseline and trails the oracle by `0.10391`.
- Ablation: full v5 success `0.79583`; best removed-component ablation success `0.73429`.
- Fixed-risk strict v5: coverage `1.00000`, success `0.79427`, collision/trap `0.03351`, support failure `0.01215`, utility `0.43183`.

## Scope

The claim is local. It does not prove real robot performance, accepted external benchmark superiority, deployable model performance, or broad dominance over all scene-graph planning systems.
