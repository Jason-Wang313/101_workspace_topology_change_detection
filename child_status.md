# Child Status

Paper: 101 workspace_topology_change_detection

Status: SUCCESS_STRONG_REVISE

Hardening version: v5 expanded

Last update: 2026-06-22

PDF: C:/Users/wangz/Downloads/101.pdf

PDF SHA256: 23709308E051A0E8AE6707EB14136BFB03AE954816511854137ABDBBF7ECBB92

Pages: 25

GitHub: https://github.com/Jason-Wang313/101_workspace_topology_change_detection

Evidence: v5 rerun with 345,600 main closed-loop rollouts, 115,200 ablation rollouts, 288,000 stress rollouts, 276,480 fixed-risk rollouts, 24 negative cases, strong non-oracle baselines, oracle reference, calibration and fixed-risk tests, generated figures, generated tables, and a 25-page manuscript with boxed citation links. The proposed `risk_calibrated_topology_belief_v5` reaches success 0.80095 versus 0.67222 for the strongest non-oracle v4 reference and 0.55191 for topological SLAM/TAMP, with lower invalid plans, collision/trap failures, support failures, ECE, regret, and higher utility.

ICLR main ready: no. All local empirical gates pass, but the scope gate fails because external robotics validation, calibrated topology-change logs, accepted high-fidelity benchmark evidence, a trained deployable checkpoint, and rollout videos are still missing.
