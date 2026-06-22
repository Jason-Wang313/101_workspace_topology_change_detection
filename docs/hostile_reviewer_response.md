# Hostile Reviewer Response

## Attack: This is not external robotics evidence.

Response: Correct. The terminal result is STRONG_REVISE, not ready. The benchmark is much stronger than the earlier archive version, but it does not replace robot hardware, accepted high-fidelity simulation, or accepted external benchmarks.

## Attack: Topological SLAM/TAMP is the real baseline.

Response: v5 includes `topological_slam_tamp`. The proposed method reaches success `0.80095` versus `0.55191` for topological SLAM/TAMP and also lowers invalid plans, collision/trap failures, support failures, ECE, regret, and negative utility.

## Attack: The strongest non-oracle competitor is the previous v4 detector.

Response: Correct, and this is reported directly. v5 reaches success `0.80095` versus `0.67222` for v4, with pairwise success margin `+0.12873`.

## Attack: The result could be a diagnostic-only win.

Response: The local evidence includes closed-loop success, invalid-plan rate, collision/trap rate, support-failure rate, regret, fixed-risk behavior, and utility, not only topology F1.

## Attack: The method may only win by abstaining or over-filtering.

Response: The fixed-risk audit reports strict v5 coverage `1.00000`, success `0.79427`, collision/trap `0.03351`, support failure `0.01215`, and utility `0.43183`; the local win is not an abstention artifact.

## Attack: What is missing for submission?

Response: Real robot or accepted external benchmark validation, calibrated change events, trained checkpoint release, rollout videos, and deeper manual related-work synthesis.
