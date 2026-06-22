# Plan

Paper 101 v5 expanded-submission rebuild executed from `docs/paper101_expanded_submission_plan_20260622.md`.

Terminal result: STRONG_REVISE.

Frozen local empirical gates passed: success, invalid-plan, collision, support, diagnostic, latency, regret, utility, calibration, ablation, stress, and fixed-risk.

Failed submission-readiness gate: scope. The artifact still lacks real robot validation, accepted high-fidelity benchmark evidence, external topology-change logs, trained checkpoints, rollout videos, and deeper manual related-work synthesis.

Next revival work:

1. Evaluate the frozen method on a real robot or accepted robotics benchmark with changing supports, passages, occlusions, reachability components, and tool-access constraints.
2. Calibrate topology-change regimes from robot logs rather than only executable surrogate distributions.
3. Replace the executable proxy with a trained graph/belief model and release checkpoints plus model cards.
4. Compare against deployed topological SLAM/TAMP, dynamic scene-graph, and neural TAMP systems under the same fixed protocol.
5. Release per-episode traces, videos, and external failure audits.
