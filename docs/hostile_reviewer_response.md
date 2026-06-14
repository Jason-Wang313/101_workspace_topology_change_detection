# Hostile Reviewer Response

## Attack: This is not external robotics evidence.

Response: Correct. The terminal result is STRONG_REVISE, not ready. The benchmark is paper-specific and rigorous locally, but it does not replace hardware or accepted external benchmarks.

## Attack: Topological SLAM/TAMP is the real baseline.

Response: v4 includes `topological_slam_tamp` as the strongest non-oracle baseline. The proposed method beats it by `0.114 +/- 0.006` success under combined stress and reduces invalid plans, collision/trap failures, and detection latency.

## Attack: The result could be a diagnostic-only win.

Response: The local evidence includes closed-loop success, invalid-plan rate, collision/trap rate, support failure, and regret, not only topology F1.

## Attack: What is missing for submission?

Response: External benchmark or robot validation, calibrated change events, trained checkpoint release, rollout videos, and deeper related-work synthesis.
